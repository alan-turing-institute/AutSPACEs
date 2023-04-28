import datetime
import json
import io
import uuid
import requests
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import ModerateExperienceForm
from .models import PublicExperience, ExperienceHistory

def is_moderator(user):
    """Return membership of moderator group."""

    try:
        group = Group.objects.get(user=user,name='Moderators')
        return bool(group)

    except Group.DoesNotExist:
        return False


def model_to_form(model, disable_moderator=False):
    """Converts Model to form."""
    model_dict = model_to_dict(model)
    model_dict["moderation_prior"] = model_dict["moderation_status"]

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
    ]:
        model_dict.pop(key, None)
    model_dict["viewable"] = True  # Only moderate viewable experiences

    return model_dict


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
        file = None
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

    combined = {k: v for k, v in data["data"].items() if k in settings.METADATA_MASK}
    # Using dict.update the metadata values will take priority
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

