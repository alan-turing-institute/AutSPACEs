import datetime
import json
import io
import uuid
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
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


def get_oh_file(ohmember, uuid):
    """Returns a single file from OpenHumans, filtered by uuid.

    Args:
        ohmember : request.user.openhumansmember
        uuid (str): unique identifier

    Raises:
        Exception: If uuid belongs to more than one file.

    Returns:
        file (dict): dictionary representation of OpenHumans file. Returns None if uuid is not matched.
    """
    files = ohmember.list_files()
    file = [f for f in files if f["metadata"]["uuid"] == uuid]

    if len(file) == 0:
        file = None
    elif len(file) > 1:
        raise Exception("duplicate uuids in open humans")

    return file[0]


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
        "drug": {"True": "drugs", "False": ""},
        "abuse": {"True": "abuse", "False": ""},
        "negbody": {"True": "negative body", "False": ""},
        "violence": {"True": "violence", "False": ""},
        "mentalhealth": {"True": "mental health", "False": ""},
        "moderation_status": {"True": "", "False": "in review"},
    }

    tags = [tag_map[k].get(str(v)) for k, v in data.items() if k in tag_map.keys()]
    if data["other"] != "":
        tags.append("Other triggering label")
    # remove empty tags
    tags = [tag for tag in tags if bool(tag) == True]
    return tags


def upload(data, uuid, ohmember):
    """Uploads a dictionary representation of an experience to open humans.

    Args:
        data (dict): an experience
        uuid (str): unique identifier
        ohmember : request.user.openhumansmember
    """

    output_json = {"data": data, "timestamp": str(datetime.datetime.now())}

    # by saving the output json into metadata we can access the fields easily through request.user.openhumansmember.list_files().
    metadata = {
        "uuid": uuid,
        "description": data.get("title_text"),
        "tags": make_tags(data),
        **output_json,
    }

    # create stream for OH upload
    output = io.StringIO()
    output.write(json.dumps(output_json))
    output.seek(0)

    ohmember.upload(
        stream=output,
        filename=f"{uuid}.json",  # filename is Autspaces_timestamp
        metadata=metadata,
    )


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


def update_public_experience_db(data, uuid, ohmember, **change_info):
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

        # Produce and add the ExperienceHistory object to the public experience
        eh = ExperienceHistory(
            experience=pe,
            change_type=change_type,
            changed_at=datetime.datetime.now(),
            changed_by=str(ohmember),
            change_comments=change_comments,
        )

        eh.save()

    else:
        delete_PE(uuid, ohmember)
