import logging

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.forms.models import model_to_dict

from .models import UserProfile
from .forms import UserProfileForm
from .helpers import (
    user_profile_exists,
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

            return redirect("users:profile")
        else:
            try:
                profile = UserProfile.objects.get(user=request.user)
                data = model_to_dict(profile)
                # If the profile has been submitted this can't be the user's first visit
                first_visit &= not profile.profile_submitted
                form = UserProfileForm(data)
            except UserProfile.DoesNotExist:
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

