import datetime
import json
import io
import uuid
import requests
import os
import textwrap
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import ModerateExperienceForm
from .models import PublicExperience, ExperienceHistory
from django.db.models import Q

def is_moderator(user):
    """Return membership of moderator group."""

    try:
        group = Group.objects.get(user=user,name='Moderators')
        return bool(group)

    except Group.DoesNotExist:
        return False


def public_experience_model_to_form(model, disable_moderator=False):
    """Converts Model to form."""
    model_dict = model_to_dict(model)
    model_dict["moderation_prior"] = model_dict["moderation_status"]

    # Copy the latest moderation reply to the form
    if (model.experience_id):
        change_reply, changed_at = get_latest_change_reply(model.experience_id)
        model_dict["moderation_reply"] = json.dumps(change_reply)

    form = ModerateExperienceForm(
        {**model_dict, "viewable": True},  # we only moderate public experiences
        disable_moderator=disable_moderator,
    )

    return form


def extract_experience_details(model):
    """
    Extract the immutable details of the story and the sharing options only.
    """
    model_dict = model_to_dict(model)

    for key in [
        "abuse",
        "violence",
        "drug",
        "mentalhealth",
        "negbody",
        "other",
        "moderation_status",
        "authorship_relation",
        "first_hand_authorship",
    ]:
        model_dict.pop(key, None)
    model_dict["viewable"] = True  # Only moderate viewable experiences

    return model_dict

def extract_authorship_details(form):
    """
    Get the mutable authorship details from the data
    """
    form.is_valid()
    # Populate with values from moderation form
    authorship_dict = {
        k: form.cleaned_data[k]
        for k in form.data.keys()
        if k in ['first_hand_authorship', 'authorship_relation']
    }
    return authorship_dict

def process_trigger_warnings(form):
    """
    Get the mutable trigger warnings from the data.
    """
    form.is_valid()
    # Populate with values from moderation form
    trigger_warning_dict = {
        k: form.cleaned_data[k]
        for k in form.data.keys()
        if k not in ["csrfmiddlewaretoken", "research"]
    }

    # Set all others as False
    for key in ["abuse", "violence", "drug", "mentalhealth", "negbody"]:
        if key not in trigger_warning_dict.keys():
            trigger_warning_dict[key] = False

    return trigger_warning_dict


def reformat_date_string(context):
    """
    Convert the date string back to a datetime object.
    """
    for file in context["files"]:
        file["created"] = datetime.datetime.strptime(
            file["created"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    return context


def get_review_status(files):
    """Given a list of files, count the number of each moderation status of the publicly viewable files

    Args:
        files (dict): list of files, which are dictionaries. See `upload()`.

    Returns:
        statuses (dict): counts of moderation statuses
    """

    status_list = [
        f["metadata"]["data"]["moderation_status"].replace(" ", "_")
        for f in files
        if f["metadata"]["data"]["viewable"]
    ]

    statuses = {f"n_{s}": status_list.count(s) for s in set(status_list)}

    statuses["n_viewable"] = len(status_list)
    statuses["n_moderated"] = status_list.count("approved") + status_list.count(
        "rejected"
    )

    return statuses


# @vcr.use_cassette("tmp/get_oh_metadata.yaml", filter_query_parameters=['access_token'])
def get_oh_metadata(ohmember, uuid):
    """Returns the metadata for a single file from OpenHumans, filtered by uuid.

    Args:
        ohmember : request.user.openhumansmember
        uuid (str): unique identifier

    Raises:
        Exception: If uuid belongs to more than one file.

    Returns:
        metadata (dict): dictionary representation of OpenHumans file metadata. Returns None if uuid is not matched.
    """
    files = ohmember.list_files()
    file = [f for f in files if f["metadata"]["uuid"] == uuid]

    if len(file) == 0:
        file = [None]
    elif len(file) > 1:
        raise Exception("duplicate uuids in open humans")

    return file[0]

# @vcr.use_cassette("tmp/get_oh_file.yaml", filter_query_parameters=['access_token'])
def get_oh_file(url):
    """Returns a single file from OpenHumans.

    Args:
        url (str): the url of the file

    Returns:
        file (dict): dictionary representation of OpenHumans file. Returns an empty dict if the file can't be accessed.
    """
    data = {}
    # Download the file from OpenHumans
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    return data

# @vcr.use_cassette("tmp/get_oh_combined.yaml", filter_query_parameters=['access_token'])
def get_oh_combined(ohmember, uuid):
    """Returns a dictionary combining file and metadata from OpenHumans, filtered by uuid.

    Args:
        ohmember : request.user.openhumansmember
        uuid (str): unique identifier

    Raises:
        Exception: If uuid belongs to more than one file.

    Returns:
        combined (dict): dictionary representation of combined OpenHumans file and metadata. Returns an empty dict if uuid is not matched.
    """
    metadata = get_oh_metadata(ohmember, uuid)

    data = {}
    url = metadata.get('download_url') if metadata else None
    # Should we do more sanity checking of the URL?
    # E.g. check it starts with https://www.openhumans.org/... ?
    if url:
        data = get_oh_file(url)

    return rebuild_experience_data(data, metadata)

def delete_single_file_and_pe(uuid, ohmember):
    """Deletes a given file id and uuid from openhumans and ensures absence from local PublicExperiences database.

    Args:

        uuid (str): unique identifier, used for PublicExperience primary key and for OpenHumans filename.
        ohmember : request.user.openhumansmember
    """

    ohmember.delete_single_file(file_basename=f"{uuid}.json")
    delete_PE(uuid, ohmember)


def make_tags(data):
    """Builds list of tags based on data."""

    tag_map = {
        "viewable": {"True": "public", "False": "not public"},
        "research": {"True": "research", "False": "non-research"},
    }

    tags = [tag_map[k].get(str(v)) for k, v in data.items() if k in tag_map.keys()]
    if data["other"] != "":
        tags.append("Other triggering label")
    # remove empty tags
    tags = [tag for tag in tags if bool(tag) == True]
    return tags

def prepare_metadata(uuid, timestring, data):
    # The description is truncated to DESCRIPTION_LEN_MAX (100) characters as
    # this is the maximum supported by OpenHumans
    return {
        "uuid": uuid,
        "description": data.get("title_text")[:settings.DESCRIPTION_LEN_MAX],
        "tags": make_tags(data),
        "timestamp": timestring,
        "data": {k: v for k, v in data.items() if k not in settings.METADATA_MASK},
    }

def upload(data, uuid, ohmember):
    """Uploads a dictionary representation of an experience to open humans.

    Args:
        data (dict): an experience
        uuid (str): unique identifier
        ohmember : request.user.openhumansmember
    """

    timestring = str(datetime.datetime.now())
    output_json = {"data": data, "timestamp": timestring}

    # by saving the output json into metadata we can access the fields easily through request.user.openhumansmember.list_files().
    metadata = prepare_metadata(uuid, timestring, data)

    # create stream for OH upload
    output = io.StringIO()
    output.write(json.dumps(output_json))
    output.seek(0)

    ohmember.upload(
        stream=output,
        filename=f"{uuid}.json",  # filename is Autspaces_timestamp
        metadata=metadata,
    )

def rebuild_experience_data(data, metadata):
    """Combines file data with metadata into a consistent format.

    In case values appear in both the file data and metadata, the
    metadata values will take priority.

    The file data should be in the following form:
    {
        "data": {
            "experience_text": "...",
            "difference_text": "...",
            "title_text": "...",
            ...
        },
        ...
    }

    The metadata should be in the following form:
    {
        "download_url": "https://www.openhumans.org/..",
        "metadata": {
            "data": {
                "other": ...,
                ...
            },
            "tags": [...],
            ...
          },
          ...
    }

    The returned structure will be in the following form:
    {
        "experience_text": "...",
        "difference_text": "...",
        "title_text": "...",
        "other": "...",
        "moderation_status": "..."
        ...
    }

    Args:
        data (dict): the file data
        metadata (dict): the metadata

    Returns:
        combined (dict): combined file and metadata dictionary
    """

    if "data" in data:
        combined = {k: v for k, v in data["data"].items() if k in settings.METADATA_MASK}
    else:
        combined = {}
    # Using dict.update the metadata values will take priority
    if metadata:
        combined.update(metadata["metadata"]["data"])
    return combined

def make_uuid():
    """Create a Universal Unique Identifier."""
    return str(uuid.uuid1())


def delete_PE(uuid, ohmember):
    """Delete Public Experience object with given UUID."""
    if PublicExperience.objects.filter(
        experience_id=uuid, open_humans_member=ohmember
    ).exists():
        PublicExperience.objects.get(
            experience_id=uuid, open_humans_member=ohmember
        ).delete()


def update_public_experience_db(data, uuid, ohmember, editing_user, **change_info):
    """Updates the public experience database for the given uuid.

    If data is tagged as viewable, an experience will be updated or inserted.
    If a data is tagged as not public, this function ensures that it is absent from the pe db.

    Args:
        data (dict): an experience
        uuid (str): unique identifier
        ohmember : request.user.openhumansmember
        moderation_status (str, optional): Defaults to 'in review'.
    """
    if data.pop("viewable", False):
        data.pop(
            "open_humans_member", None
        )  # Remove from dict as needs to be an object not string
        data.pop(
            "experience_id", None
        )  # Remove from dict as needs to be an object not string
        data.pop("moderation_comments", None)  # Only need when moderating

        pe = PublicExperience(open_humans_member=ohmember, experience_id=uuid, **data)

        # .save() updates if primary key exists, inserts otherwise.
        pe.save()

        # If no change info has been sent then it's either new or being edited by user
        if not change_info:
            change_reply = ""
            if pe.experiencehistory_set.count() == 0:
                change_type = "Make Public"
                change_comments = "Story flagged to be shared on AutSPACE website"
            else:
                change_type = "Edit"
                change_comments = "Story edited"
        else:
            change_type = change_info.get("change_type", "Unknown Change")
            change_comments = change_info.get("change_comments", "No Comment Made")
            if change_comments == "":
                change_comments = "No Comment Made"
            change_reply = change_info.get("change_reply", "")

        # Produce and add the ExperienceHistory object to the public experience
        eh = ExperienceHistory(
            experience=pe,
            change_type=change_type,
            changed_at=datetime.datetime.now(),
            changed_by=editing_user,
            change_comments=change_comments,
            change_reply=change_reply,
        )

        eh.save()

    else:
        delete_PE(uuid, ohmember)

def moderate_page(request, status, experiences):
    """
    View containing lists of the given Public Experiences

    A helper function for generating the Moderation pages.
    """
    # Check to see if a search has been performed
    searched = request.GET.get("searched", False)

    if searched:
        # If there's a search term, additionally filter on it too
        experiences = experiences.filter(
            Q(title_text__icontains=searched)
            | Q(experience_text__icontains=searched)
            | Q(difference_text__icontains=searched)
        )

    paginator = Paginator(experiences, settings.EXPERIENCES_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_obj.page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    page_obj.offset = page_obj.start_index() - 1

    unreviewed = PublicExperience.objects.filter(
        Q(moderation_status="not reviewed")
    ).count()
    inreview = PublicExperience.objects.filter(
        Q(moderation_status="in review")
    ).count()
    approved = PublicExperience.objects.filter(
        Q(moderation_status="approved")
    ).count()
    rejected = PublicExperience.objects.filter(
        Q(moderation_status="rejected")
    ).count()

    subtitle = {
        "pending": "Experiences for Moderation",
        "approved": "Approved Experiences",
        "rejected": "Rejected Experiences",
    }.get(status, "Moderation")

    return render(
        request,
        "main/moderation_list.html",
        context={
            "subtitle": subtitle,
            "status": status,
            "page_obj": page_obj,
            "unreviewed": unreviewed,
            "inreview": inreview,
            "approved": approved,
            "rejected": rejected,
            "searched": searched if searched else "",
            "params": "?status=" + status + (("&searched=" + searched) if searched else ""),
        },
    )

def choose_moderation_redirect(moderation_prior):
    """
    Selects an appropriate redirect from the moderate story form

    When a moderator submits a story moderation, the form redirects
    to different places depending on where the user requested the
    moderation from. This helper function returns the place to
    redurect to.
    """
    return moderation_prior if moderation_prior in ["approved", "rejected"] else "pending"


def extract_triggers_to_show(allowed_triggers):
    """
    Generate a list of triggering labels that the user has opted in to seeing
    """

    all_triggers = {'abuse', 'violence', 'drug', 'mentalhealth', 'negbody', 'other'}
    triggers_to_show = list(all_triggers.intersection(allowed_triggers))
    return(triggers_to_show)

def show_filter(experiences, triggers_to_show):
    """
    Explicitly look for experiences with the trigger tags from the triggers_to_show list
    """
    tmp_dict = {}
    for t in triggers_to_show:
        tmp_dict[t] = True


    experiences.filter(Q(**tmp_dict) | Q(abuse=False))

    for trigger in triggers_to_show:
        if trigger == "abuse":
            experiences = experiences.filter(Q(abuse=True) | Q(abuse=False))
        if trigger == "violence":
            experiences =  experiences.filter(Q(violence=True) | Q(violence=False))
        if trigger == "drug":
            experiences =  experiences.filter(Q(drug=True) | Q(drug=False))
        if trigger == "mentalhealth":
            experiences =  experiences.filter(Q(mentalhealth=True) | Q(mentalhealth=False))
        if trigger == "negbody":
            experiences =  experiences.filter(Q(negbody=True) | Q(negbody=False))
        if trigger == "other":
            experiences = experiences.filter(~Q(other="") | Q(other=""))

    return experiences

def no_show_filter(experiences, triggers_to_show):
    """
    Explicitly omit stories that aren't in the triggers_to_show list
    This coupled with the show_filter function allows for experiences with multiple
    trigger warnings to be shown
    """
    if "abuse" not in triggers_to_show:
        experiences = experiences.filter(Q(abuse=False))
    if "violence" not in triggers_to_show:
        experiences = experiences.filter(Q(violence=False))
    if "drug" not in triggers_to_show:
        experiences = experiences.filter(Q(drug=False))
    if "mentalhealth" not in triggers_to_show:
        experiences = experiences.filter(Q(mentalhealth=False))
    if "negbody" not in triggers_to_show:
        experiences = experiences.filter(Q(negbody=False))
    if "other" not in triggers_to_show:
        experiences = experiences.filter(Q(other=""))

    return experiences




def expand_filter(experiences, triggers_to_show):
    """
    Expand the QuerySet.
    Recieves the filtered(allowed) stories and filters by the model fields which
    correspond to the triggering content labels
    """

    experiences = show_filter(experiences, triggers_to_show)
    experiences = no_show_filter(experiences, triggers_to_show)

    return experiences

def filter_by_tag(files, tag):
    """ Filter stories by tag """
    return [file for file in files if tag in file['metadata']['tags']]

def filter_by_moderation_status(files, status):
    """ Filter stories by moderation status """
    return [file for file in files if file['metadata']['data']['moderation_status'] == status]

def filter_in_review(files):
    """ Filter stories that are in review """
    return [file for file in files if file['metadata']['data']['moderation_status'] == "in review" or
            (file['metadata']['data']['moderation_status'] == "not reviewed" and "public" in file['metadata']['tags'])]

def paginate_stories(request, paginator, page):
    """ Paginate stories """
    stories_page = request.GET.get(page)
    stories = paginator.get_page(stories_page)
    # show ... when there are too many pages
    stories.page_range = paginator.get_elided_page_range(stories.number, on_each_side=2, on_ends=1)
    stories.offset = stories.start_index() - 1
    return stories

def number_stories(stories, items_per_page):
    """
    Adds a number field to each story for continuous numbering across pages

    Stories can be either PublicExperience objects (for the shared stories page)
    or dictionaries (for the my_stories page)
    """
    # Calculate the start index for the current page
    start_index = (stories.number - 1) * items_per_page
    # Add the start index to each experience in page_experiences
    for i, story in enumerate(stories, start=start_index):
        if isinstance(story, PublicExperience):
            story.number = i + 1
        elif isinstance(story, dict):
            story["number"] = i + 1
        else:
            raise TypeError(f'Unexpected type for story: {type(story)}')
    return stories

def structure_change_reply(reply):
    structured = None
    try:
        structured = json.loads(reply)
    except json.JSONDecodeError:
        if reply != "":
            text = '[{{"reason": "Text", "text":"{}"}}]'.format(reply)
            structured = json.loads(text)
        else:
            structured = ""
    return structured

def get_latest_change_reply(experience_id):
    change_reply = ""
    changed_at = None
    # We catch exceptions in case the experience doesn't exist
    # in the local database
    try:
        pe = PublicExperience.objects.get(experience_id=experience_id)
        if pe.experiencehistory_set.count() > 0:
            latest = pe.experiencehistory_set.order_by(
                "-changed_at"
            )[0]
            change_reply = structure_change_reply(latest.change_reply)
            changed_at = latest.changed_at
    except PublicExperience.DoesNotExist:
        pass

    return change_reply, changed_at

def get_message(file_name):
    """
    Loads a message to be sent to the user.

    The first line of the file should contain the subject. Subsequent lines
    will comprise the message body.

    Args:
        file_name: the leaf name of the file to load.
    Returns:
        subject and body of the message.
    """
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, file_name)
    subject = None
    message = ""
    try:
        with open(file_path, "r") as f:
            subject = f.readline()
            for line in f:
                message += line
    except IOError as e:
        print("Exception when opening moderation message: {}".format(str(e)))
        message = None
    return subject, message

def message_wrap(text, width):
    """
    Wrap the text to the given width, but retain paragraph breaks (empty lines)
    """
    return "\n".join(map(lambda para: "\n".join(textwrap.wrap(para, width)), text.split("\n")))

def experience_titles_for_session(files):
    """
    take a member.list_files() list of files and add them to dict
    of the form 
    {"titles":{
        "uuid": "title",
        "uuid2": "title2"
    }}
    To be added to session
    """
    titles = {}
    for f in files:
        if "uuid" in f['metadata'].keys():
            titles[f['metadata']['uuid']] = f['metadata']['description']
    return titles

def number_by_review_status(files):
    """
    Return a dictionary of review status: number for the My Stories page
    """
    list_status = ["approved", "not_reviewed", "rejected", "in_review"]
    status = {s: 0 for s in list_status}

    for f in files:
        s = f['metadata']['data']['moderation_status']
        status[s.replace(" ","_")] = status[s.replace(" ","_")] + 1

    # Get the private stories
    private = 0
    for f in files:
        if not f['metadata']['data']['viewable']:
            private += 1

    status["private"] = private
    status["not_reviewed"] = status["not_reviewed"] - private

    status["moderated"] = status["approved"] + status["rejected"]


    return status

def most_recent_exp_history(ohm):
    """
    Return the most recent Moderate Experience History for the user
    """

    try:
        exp_hist = ExperienceHistory.objects.filter(Q(experience__open_humans_member=ohm) 
                                     & Q(change_type="Moderate")).latest("changed_at")
        return exp_hist

    except ExperienceHistory.DoesNotExist:
        return None


    
    