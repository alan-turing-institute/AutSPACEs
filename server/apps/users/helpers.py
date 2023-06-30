from django.contrib.auth.models import User
from .models import UserProfile

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
    the profile page (because they might legitimately want the profile to be
    emtpy).

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

