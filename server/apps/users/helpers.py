from django.contrib.auth.models import User
from .models import UserProfile
from server.apps.main.models import PublicExperience

def user_profile_exists(user):
    """
    Determines whether the user profile for the user exists. If it doesn't
    exist, it means that this is a first-time login

    A default profile is created immediately when entering the user profile
    page, so this will return True until that point and False afterwards.

    Args:
        user: request.user

    Returns:
        True if this is the first time the user has logged in, False o/w.
    """
    uo = UserProfile.objects.filter(user=user)
    return (uo.count() > 0)

def user_submitted_profile(user):
    """
    Determines whether the user has ever hit the Submit button on the profile page.

    This is the best indication we have of whether the user has ever filled out
    the profile page, because they'll be blocked from submitting it if they've
    filled out the required fields and all others are optional.

    Args:
        user: request.user

    Returns:
        True if the user has ever submitted a profile update, False o/w.
    """
    try:
        submitted = UserProfile.objects.get(user=user).profile_submitted
    except UserProfile.DoesNotExist:
        submitted = False
    return submitted

def get_user_profile(user):
    """
    Attempts to get the profile for a user.

    Args:
        user: request.user

    Returns:
        The UserProfile associated with the user if it exists, None otherwise
    """
    try:
        uo = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        uo = None
    return uo

def delete_user(user, delete_oh_data):
    """
    Deletes the user and all data associated with it.

    Args:
        delete_oh_data: True if stories on OpenHumans should also be deleted

    Returns:
        None
    """
    ohmember = user.openhumansmember

    # Delete the stories from the OpenHumans database
    if delete_oh_data:
        ohmember.delete_all_files()

    # Delete the actual user
    user.delete()

