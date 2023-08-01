import io
import json
import logging
import vcr

import requests
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from openhumans.models import OpenHumansMember
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .models import PublicExperience
from server.apps.users.models import UserProfile

from .forms import ShareExperienceForm, ModerateExperienceForm

from django.contrib import messages

from .helpers import (
    is_moderator,
    public_experience_model_to_form,
    extract_experience_details,
    reformat_date_string,
    get_review_status,
    get_oh_combined,
    delete_single_file_and_pe,
    upload,
    rebuild_experience_data,
    make_uuid,
    delete_PE,
    update_public_experience_db,
    process_trigger_warnings,
    moderate_page,
    choose_moderation_redirect,
    extract_triggers_to_show,
    expand_filter,
    filter_by_tag,
    filter_by_moderation_status,
    filter_in_review,
    paginate_stories,
    get_latest_change_reply,
    structure_change_reply,
    number_stories,
    get_message,
    message_wrap,
)

from server.apps.users.helpers import (
    user_profile_exists,
    get_user_profile,
)

logger = logging.getLogger(__name__)


def confirmation_page(request):
    """
    Confirmation Page For App.
    """
    if request.user.is_authenticated:
        return render(request, "main/confirmation_page.html")
    else:
        return redirect("main:overview")


def about_us(request):
    return render(request, "main/about_us.html")


def what_autism_is(request):
    return render(request, "main/what_autism_is.html")


def help(request):
    return render(request, "main/help.html")


def code_of_conduct(request):
    return render(request, "main/code_of_conduct.html")


def edit_experience(request):
    return render(request, "main/share_experiences.html")


def signup(request):
    return render(request, "main/signup.html")


def registration(request):
    registration_status = True
    print(registration_status)
    return render(request, "main/registration.html", {"page_status": "registration"})


def logout_user(request):
    """
    Logout user
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


def index(request):
    """
    Starting page for app.
    """
    auth_url = OpenHumansMember.get_auth_url()
    context = {"auth_url": auth_url, "oh_proj_page": settings.OH_PROJ_PAGE}
    if request.user.is_authenticated:
        return redirect("main:overview")
    return render(request, "main/home.html", context=context)


# @vcr.use_cassette("tmp/overview.yaml", filter_query_parameters=['access_token'])
def overview(request):
    """
    Overview page for logged in users directs to home, otherwise to index.
    """
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {
            "oh_id": oh_member.oh_id,
            "oh_member": oh_member,
            "oh_user": oh_member.user,
            "oh_proj_page": settings.OH_PROJ_PAGE,
        }
        return render(request, "main/home.html", context=context)
    return redirect("index")

def login_user(request):
    """
    Page the user arrives at immediately after logging in, expected to
    immediately redirect to somewhere else.
    """
    if request.user.is_authenticated:
        if not user_profile_exists(user=request.user):
            # This is the first time we've logged into the site
            # We use update_or_create() rather than create() to avoid a race
            # condition on existence
            UserProfile.objects.update_or_create(user=request.user)
            return redirect("users:greetings")

    return redirect("main:overview")

# @vcr.use_cassette("server/apps/main/tests/fixtures/share_exp.yaml", filter_query_parameters=['access_token', 'AWSAccessKeyId'])
def share_experience(request, uuid=False):
    """
    Form where users can share details of their experiences.
    """
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated:
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = ShareExperienceForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                if uuid:
                    # we will be here if we are editing a record that already exists
                    # for OH we need to Delete before reupload.
                    request.user.openhumansmember.delete_single_file(
                        file_basename=f"{uuid}.json"
                    )
                else:
                    uuid = make_uuid()

                upload(
                    data=form.cleaned_data,
                    uuid=uuid,
                    ohmember=request.user.openhumansmember,
                )

                # for Public Experience we need to check if it's viewable and update accordingly.
                update_public_experience_db(
                    data=form.cleaned_data,
                    uuid=uuid,
                    ohmember=request.user.openhumansmember,
                    editing_user=request.user.openhumansmember,
                )

                # redirect to a new URL:
                return redirect("main:confirm_page")
            # If form is invalid raise errors back to user
            else:
                for field in form:
                    for error in field.errors:
                        if field != "__all__":
                            messages.add_message(
                                request,
                                messages.WARNING,
                                "{}: {}".format(field.label, error),
                            )

                if uuid:  # check if editing existing exp
                    moderation_status = PublicExperience.objects.get(
                        experience_id=uuid
                    ).moderation_status
                    title = "Edit experience"
                    change_reply, changed_at = get_latest_change_reply(uuid)
                else:  # or creating new one
                    moderation_status = "not reviewed"
                    title = "Share experience"
                    change_reply = ""
                    changed_at = None
                return render(
                    request,
                    "main/share_experiences.html",
                    {
                        "form": form,
                        "uuid": uuid,
                        "title": title,
                        "moderation_status": moderation_status,
                        "change_reply": change_reply,
                        "changed_at": changed_at,
                    },
                )
        # if a GET (or any other method) we'll either create a blank form or
        # prepopulate form based on existing data.
        else:
            if uuid:
                # return data from oh.
                data = get_oh_combined(
                    ohmember=request.user.openhumansmember, uuid=uuid
                )
                form = ShareExperienceForm(data)
                title = "Edit experience"
                moderation_status = data.get("moderation_status", "not reviewed")
                change_reply, changed_at = get_latest_change_reply(uuid)
            else:
                form = ShareExperienceForm()
                title = "Share experience"
                moderation_status = "not reviewed"
                change_reply = ""
                changed_at = None

            return render(
                request,
                "main/share_experiences.html",
                {
                    "form": form,
                    "uuid": uuid,
                    "title": title,
                    "moderation_status": moderation_status,
                    "change_reply": change_reply,
                    "changed_at": changed_at,
                },
            )

    else:
        return redirect("index")


# @vcr.use_cassette("server/apps/main/tests/fixtures/view_exp.yaml", filter_query_parameters=['access_token', 'AWSAccessKeyId'])
def view_experience(request, uuid):
    """
    Show a read-only view of the story in a form.
    """
    if request.user.is_authenticated:
        # return data from oh.
        data = get_oh_combined(ohmember=request.user.openhumansmember, uuid=uuid)
        form = ShareExperienceForm(data, disable_all=True)
        change_reply, changed_at = get_latest_change_reply(uuid)
        return render(
            request,
            "main/share_experiences.html",
            {
                "form": form,
                "uuid": uuid,
                "readonly": True,
                "change_reply": change_reply,
                "changed_at": changed_at,
                "show_moderation_status": False,
                "title": "View experience",
            },
        )
    else:
        return redirect("main:overview")


# @vcr.use_cassette("server/apps/main/tests/fixtures/delete_exp.yaml", filter_query_parameters=['access_token'])
def delete_experience(request, uuid, title):
    """
    Delete experience from PE databacse and OH
    """
    # TODO: we currently are passing title via url because it is nice to display it in the confirmation. We could improve the deletion process by having a javascript layover.

    if request.user.is_authenticated:
        if request.method == "POST":
            delete_single_file_and_pe(uuid=uuid, ohmember=request.user.openhumansmember)

            return render(request, "main/deletion_success.html", {"title": title})

        else:
            return render(
                request,
                "main/deletion_confirmation.html",
                {"title": title, "uuid": uuid},
            )
    else:
        return redirect("index")


def list_public_experiences(request):
    """
    Returns, in the context, experiences that are
    1) listed public,
    2) approved,
    3) searched,
    4) abide by triggering label toggle.
    """

    # Find all approved stories
    experiences = PublicExperience.objects.filter(moderation_status="approved")

    # Default is to show non-triggering content only
    all_triggers = request.GET.get("all_triggers", False)

    if all_triggers:
        allowed_triggers = {
            "abuse",
            "violence",
            "drug",
            "mentalhealth",
            "negbody",
            "other",
        }
    else:
        # Check the allowed triggers
        allowed_triggers = set(request.GET.keys())

    if request.user.is_authenticated and "searched" not in request.GET:
        profile = get_user_profile(request.user)
        if profile:
            user_data = model_to_dict(profile)
            allowed_triggers = set([key for key in user_data if user_data[key]])

    # Get a list of allowed triggers
    triggers_to_show = extract_triggers_to_show(allowed_triggers)

    tts = {}
    for trigger in triggers_to_show:
        trigger_check = f"check{trigger}"
        tts[trigger_check] = True

    experiences = expand_filter(experiences, triggers_to_show)

    # Check to see if a search has been performed
    searched = request.GET.get("searched", False)

    search_context = {}
    # Only search through approved stories
    if searched:
        # search within all approved stories regardless of triggering status
        experiences = experiences.filter(
            Q(title_text__icontains=searched)
            | Q(experience_text__icontains=searched)
            | Q(difference_text__icontains=searched)
        )
        search_context["searched"] = searched

    #  Define the number of experiences to show per page
    items_per_page = settings.EXPERIENCES_PER_PAGE

    # Create a Paginator object, order by time of creation to avoid pagination issues
    paginator = Paginator(experiences.order_by("created_at"), items_per_page)
    # Paginate experiences
    page_experiences = paginate_stories(request, paginator, "page")
    # Set continuous numbering across pages
    page_experiences = number_stories(page_experiences, items_per_page)

    exp_context = {"experiences": page_experiences}

    context = {**tts, **exp_context, **search_context}

    # Standard page showing all moderated stories
    return render(request, "main/experiences_page.html", context=context)


def moderate_public_experiences(request):
    """
    View containing lists of all Public Experiences with their applicable moderation status
    """
    if request.user.is_authenticated and is_moderator(request.user):
        unreviewed_experiences = PublicExperience.objects.filter(
            moderation_status="not reviewed"
        )
        previously_reviewed_experiences = PublicExperience.objects.filter(
            ~Q(moderation_status="not reviewed")
        )
        return render(
            request,
            "main/moderate_public_experiences.html",
            context={
                "unreviewed_experiences": unreviewed_experiences,
                "previously_reviewed_experiences": previously_reviewed_experiences,
            },
        )
    else:
        return redirect("main:overview")


def moderation_list(request):
    """
    View containing lists of Public Experiences with a given status

    When status is "pending" this includes experiences marked as "unmoderated"
    or "in review".

    When status is "approved" it includes experiences marked as "approved".

    When status is "rejected" it includes experiences marked as "rejected".
    """
    if request.user.is_authenticated and is_moderator(request.user):
        status = request.GET.get("status", "pending")
        if status not in ["pending", "approved", "rejected"]:
            status = "pending"

        if status == "approved":
            # Search through approved experiences
            experiences = PublicExperience.objects.filter(
                moderation_status="approved"
            ).order_by("created_at")
        elif status == "rejected":
            # Search through rejected experiences
            experiences = PublicExperience.objects.filter(
                moderation_status="rejected"
            ).order_by("created_at")
        else:
            # Search through unreviewed or in review experiences
            experiences = PublicExperience.objects.filter(
                Q(moderation_status="not reviewed") | Q(moderation_status="in review")
            ).order_by("created_at")

        return moderate_page(request, status, experiences)
    else:
        return redirect("main:overview")

#@vcr.use_cassette("server/apps/main/tests/fixtures/pag_mystories.yaml", filter_query_parameters=['access_token'])
def my_stories(request):
    """
    List all stories that are associated with the OpenHumans project page.
    Including those which are not-shareable on the website
    """
    if request.user.is_authenticated:
        files = request.user.openhumansmember.list_files()
        context = {"files": files}
        context = reformat_date_string(context)

        # Define the number of items per page
        items_per_page = settings.EXPERIENCES_PER_PAGE

        # For each category, filter stories, create pagination and add continuous numbering

        # Public stories
        paginator_public = Paginator(
            filter_by_tag(filter_by_moderation_status(files, "approved"), "public"),
            items_per_page,
        )
        public_stories = paginate_stories(request, paginator_public, "page_public")
        public_stories = number_stories(public_stories, items_per_page)

        # In review stories
        paginator_review = Paginator(
            filter_in_review(filter_by_tag(files, "public")), items_per_page
        )
        in_review_stories = paginate_stories(request, paginator_review, "page_review")
        in_review_stories = number_stories(in_review_stories, items_per_page)

        # Rejected stories
        paginator_rejected = Paginator(
            filter_by_moderation_status(files, "rejected"), items_per_page
        )
        rejected_stories = paginate_stories(request, paginator_rejected, "page_rejected")
        rejected_stories = number_stories(rejected_stories, items_per_page)

        # Private stories
        paginator_private = Paginator(
            filter_by_tag(files, "not public"), items_per_page
        )
        private_stories = paginate_stories(request, paginator_private, "page_private")
        private_stories = number_stories(private_stories, items_per_page)

        return render(
            request,
            "main/my_stories.html",
            context={
                "public_stories": public_stories,
                "in_review_stories": in_review_stories,
                "rejected_stories": rejected_stories,
                "private_stories": private_stories,
            },
        )
    else:
        return redirect("main:overview")

def moderate_experience(request, uuid):
    """
    Moderate a single experience.

    If the moderation status changes to approved or rejected, a message will be
    sent to users who opt to receive them.

    The message is stored in the file "server/apps/main/mod_message.txt" in the
    following format:

    1. First line is the message subject.
    2. All following lines are the message body.
    3. The following substitutions will be made:
         i. {story} - the URL of the view story page for this story.
        ii. {profile} - the URL of the user's profile page.
       iii. {title} - the title of the story.
        iv. {status} - the new review status (Accepted, Rejected} of the story.
    4. Paragraphs in the body of the message will be reformatted to a width of
       80 charachters.
    """
    if request.user.is_authenticated and is_moderator(request.user):
        public_experience = PublicExperience.objects.get(experience_id=uuid)
        if request.method == "POST":
            # get the data from the model
            form = ModerateExperienceForm(request.POST)
            if form.is_valid():
                # Get the (immutable) experience data
                unchanged_experience_details = extract_experience_details(public_experience)
                # Get the (mutable) trigger warnings
                trigger_details = process_trigger_warnings(form)

                # validate
                data = {**unchanged_experience_details, **trigger_details}

                moderation_comments = data.pop("moderation_comments", None)
                moderation_reply = data.pop("moderation_reply", "")
                moderation_prior = data.pop("moderation_prior", "not moderated")

                # get the users OH member id from the model
                user_OH_member = public_experience.open_humans_member

                # wrap in try/except in case user writing experience originally has left AutSPACEs
                try:
                    user_OH_member.delete_single_file(file_basename=f"{uuid}.json")
                    upload(data, uuid, ohmember=user_OH_member)
                    # update the PE object
                    update_public_experience_db(
                        data,
                        uuid,
                        ohmember=user_OH_member,
                        editing_user=request.user.openhumansmember,
                        change_type="Moderate",
                        change_comments=moderation_comments,
                        change_reply=moderation_reply,
                    )
                except Exception:
                    # if user writing E has deauthorized autspaces, delete public experience
                    delete_PE(uuid=uuid, ohmember=user_OH_member)

                # send a message to the author if they've requested it
                moderation_status = data.get("moderation_status", "")
                moderation_string = moderation_status.title()

                profile = get_user_profile(user=request.user)
                if (profile and profile.comms_review and moderation_prior != moderation_status
                    and moderation_status in ["approved", "rejected"]):
                    story_url = "{}/main/view/{}".format(settings.OPENHUMANS_APP_BASE_URL,
                        public_experience.experience_id)
                    profile_url = "{}/users/profile/".format(settings.OPENHUMANS_APP_BASE_URL)
                    subject, message = get_message("mod_message.txt")
                    if subject and message:
                        substitutes = {
                            "story": story_url,
                            "profile": profile_url,
                            "title": public_experience.title_text,
                            "status": moderation_string,
                        }
                        subject = subject.format(**substitutes)
                        message = message.format(**substitutes)
                        message = message_wrap(message, 80)
                        request.user.openhumansmember.message(subject, message)

                # redirect to a new URL:
                status = choose_moderation_redirect(moderation_prior)
                return redirect(
                    "{}?status={}".format(reverse("main:moderation_list"), status)
                )
            else:
                # Form didn't validate correctly
                for error in form.non_field_errors():
                    messages.add_message(
                        request,
                        messages.WARNING,
                        "{}".format(error)
                    )

                experience_title = public_experience.title_text
                experience_text = public_experience.experience_text
                experience_difference = public_experience.difference_text
                experience_history = public_experience.experiencehistory_set.all().order_by(
                    "-changed_at"
                )
                for history_item in experience_history:
                    history_item.change_reply = structure_change_reply(history_item.change_reply)

                return render(
                    request,
                    "main/moderate_experience.html",
                    {
                        "form": form,
                        "uuid": uuid,
                        "experience_title": experience_title,
                        "experience_text": experience_text,
                        "experience_difference": experience_difference,
                        "experience_history": experience_history,
                        "show_moderation_status": True,
                        "title": "Moderate experience",
                    },
                )

        else:
            experience_title = public_experience.title_text
            experience_text = public_experience.experience_text
            experience_difference = public_experience.difference_text
            experience_history = public_experience.experiencehistory_set.all().order_by(
                "-changed_at"
            )
            for history_item in experience_history:
                history_item.change_reply = structure_change_reply(history_item.change_reply)

            form = public_experience_model_to_form(public_experience, disable_moderator=True)
            return render(
                request,
                "main/moderate_experience.html",
                {
                    "form": form,
                    "uuid": uuid,
                    "experience_title": experience_title,
                    "experience_text": experience_text,
                    "experience_difference": experience_difference,
                    "experience_history": experience_history,
                    "show_moderation_status": True,
                    "title": "Moderate experience",
                },
            )
    else:
        return redirect("index")


def single_story(request, uuid):
    """
    Returns a single page with one story on it
    """
    # Must have both the specified UUID and be approved otherwise will redirect
    # Should only be one result if not redirect
    try:
        experience = PublicExperience.objects.get(
            experience_id=uuid, moderation_status="approved"
        )
        title = experience.title_text
        exp_context = {"experience": experience}
        title_context = {"title": title}
        context = {**exp_context, **title_context}
        return render(request, "main/single_story.html", context=context)
    except ObjectDoesNotExist:
        return redirect("main:overview")
