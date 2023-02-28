import io
import json
import logging

import requests
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from openhumans.models import OpenHumansMember
from django.db.models import Q

from .models import PublicExperience

from .forms import ShareExperienceForm, ModerateExperienceForm

from .helpers import (
    is_moderator,
    model_to_form,
    extract_experience_details,
    reformat_date_string,
    get_review_status,
    get_oh_file,
    delete_single_file_and_pe,
    upload,
    make_uuid,
    delete_PE,
    update_public_experience_db,
    process_trigger_warnings,
)

logger = logging.getLogger(__name__)


def confirmation_page(request):
    """
    Confirmation Page For App.
    """
    return render(request, "main/confirmation_page.html")


def about_us(request):
    return render(request, "main/about_us.html")


def navigation(request):
    return render(request, "main/navigation.html")


def what_autism_is(request):
    return render(request, "main/what_autism_is.html")


def footer(request):
    return render(request, "main/footer.html")


def signup_frame4_test(request):
    return render(request, "main/signup1.html")


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


def overview(request):
    """
    Overview page for logged in users directs to home, otherwise to index.
    """
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {
            "oh_id": oh_member.oh_id,
            "oh_member": oh_member,
            "oh_proj_page": settings.OH_PROJ_PAGE,
        }
        return render(request, "main/home.html", context=context)
    return redirect("index")


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
                )

                # redirect to a new URL:
                return redirect("main:confirm_page")

        # if a GET (or any other method) we'll create a blank form
        else:

            if uuid:
                # return data from oh.
                data = get_oh_file(ohmember=request.user.openhumansmember, uuid=uuid)
                form = ShareExperienceForm(data["metadata"]["data"])
                title = "Edit experience"

            else:
                form = ShareExperienceForm()
                title = "Share experience"

            return render(
                request,
                "main/share_experiences.html",
                {"form": form, "uuid": uuid, "title": title},
            )

    else:
        return redirect("index")


def view_experience(request, uuid):
    """
    Show a read-only view of the story in a form.
    """
    if request.user.is_authenticated:
        # return data from oh.
        data = get_oh_file(ohmember=request.user.openhumansmember, uuid=uuid)
        form = ShareExperienceForm(data["metadata"]["data"], disable_all=True)
        return render(
            request,
            "main/share_experiences.html",
            {
                "form": form,
                "uuid": uuid,
                "readonly": True,
                "show_moderation_status": False,
                "title": "View experience",
            },
        )
    else:
        redirect("index")


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

    experiences = PublicExperience.objects.filter(moderation_status="approved")

    # Check to see if a search has been performed
    searched = request.GET.get("searched", False)

    # Only search through approved stories
    if searched:

        # search within all approved stories regardless of triggering status

        experiences = experiences.filter(
            Q(title_text__icontains=searched)
            | Q(experience_text__icontains=searched)
            | Q(difference_text__icontains=searched)
        )

    # If the triggering stories flag is checked - perform an additional filter to remove triggering stories
    trigger_label = request.GET.get("triggering_stories", False)

    if trigger_label:
        experiences = experiences.filter(
            Q(abuse=False)
            & Q(violence=False)
            & Q(drug=False)
            & Q(mentalhealth=False)
            & Q(negbody=False)
            & Q(other="")
        )

    # Standard page showing all moderated stories
    return render(
        request, "main/experiences_page.html", context={"experiences": experiences}
    )


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


def review_experience(request, experience_id):
    experience = PublicExperience.objects.get(experience_id=experience_id)
    experience.approved = "approved"
    experience.save()
    return redirect("moderate_public_experiences")


def my_stories(request):
    """
    List all stories that are associated with the OpenHumans proejct page.
    Including those which are not-shareable on the website
    """
    if request.user.is_authenticated:
        context = {"files": request.user.openhumansmember.list_files()}
        context = reformat_date_string(context)
        statuses = get_review_status(context["files"])
        context = {**context, **statuses}
        return render(request, "main/my_stories.html", context)
    else:
        return redirect("main:overview")


def moderate_experience(request, uuid):
    """Moderate a single experience."""
    if request.user.is_authenticated and is_moderator(request.user):
        model = PublicExperience.objects.get(experience_id=uuid)
        if request.method == "POST":
            # get the data from the model
            moderated_form = ModerateExperienceForm(request.POST)
            moderated_form.is_valid()

            # Get the (immutable) experience data
            unchanged_experience_details = extract_experience_details(model)
            # Get the (mutable) trigger warnings
            trigger_details = process_trigger_warnings(moderated_form)

            # validate
            data = {**unchanged_experience_details, **trigger_details}

            moderation_comments = data.pop("moderation_comments", None)

            # get the users OH member id from the model
            user_OH_member = model.open_humans_member

            # wrap in try/except in case user writing experience originally has left AutSPACEs
            try:
                user_OH_member.delete_single_file(file_basename=f"{uuid}.json")
                upload(data, uuid, ohmember=user_OH_member)
                # update the PE object
                update_public_experience_db(
                    data,
                    uuid,
                    ohmember=user_OH_member,
                    change_type="Moderate",
                    change_comments=moderation_comments,
                )
            except Exception:
                # if user writing E has deauthorized autspaces, delete public experience
                delete_PE(uuid=uuid, ohmember=user_OH_member)
            # redirect to a new URL:
            return redirect("main:moderate_public_experiences")

        else:
            experience_title = model.title_text
            experience_text = model.experience_text
            experience_difference = model.difference_text
            experience_history = model.experiencehistory_set.all().order_by(
                "changed_at"
            )

            form = model_to_form(model, disable_moderator=True)
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
        redirect("index")
