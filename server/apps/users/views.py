import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth import logout

from .models import UserProfile
from .forms import (
    UserProfileForm,
    UserProfileDeleteForm,
)
from .helpers import (
    user_profile_exists,
    get_user_profile,
    delete_user,
    update_session_success_or_confirm,
)


logger = logging.getLogger(__name__)

def user_profile(request, first_visit=False):
    """
    User profile page.
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            form = UserProfileForm(request.POST)

            if form.is_valid():
                # Update the status to indicate the user has submitted at least once
                form.cleaned_data["profile_submitted"] = True
                UserProfile.objects.update_or_create(user=request.user, defaults=form.cleaned_data)

                success_confirm_dict = update_session_success_or_confirm(source="profile")

                for key in success_confirm_dict.keys():
                    if key in request.session:
                        del request.session[key]
                    request.session[key] = success_confirm_dict[key]

            return redirect("main:success_confirm")
        else:
            profile = get_user_profile(request.user)
            if profile:
                data = model_to_dict(profile)
                # If the profile has been submitted this can't be the user's first visit
                first_visit &= not profile.profile_submitted
                form = UserProfileForm(data)
            else:
                form = UserProfileForm()
            oh_member = request.user.openhumansmember
            return render(
                request, "users/profile.html", {
                    "title": "Profile",
                    "form": form,
                    "oh_id": oh_member.oh_id,
                    "first_visit": first_visit,
                    "request_profile": False,
                })
    else:
        return redirect("index")

def user_profile_delete(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        if request.method == "POST":
            form = UserProfileDeleteForm(request.POST)

            if form.is_valid():
                # Delete all the user's data
                delete_oh_data = form.cleaned_data['delete_oh_data']
                delete_user(request.user, delete_oh_data)
                # Log the user out. That's it.
                logout(request)
                # Say goodbye.
                return render(
                    request, "users/goodbye.html", {
                        "title": "Profile Deleted",
                        "delete_oh_data": delete_oh_data,
                    })
        else:
            form = UserProfileDeleteForm()

        return render(
            request, "users/delete.html", {
                "title": "Delete profile",
                "form": form,
                "oh_id": oh_member.oh_id,
            })

    else:
        return redirect("index")
