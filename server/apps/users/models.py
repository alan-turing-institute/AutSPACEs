from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Holds profile information about a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_submitted = models.BooleanField(default=False)
    age_bracket = models.TextField(default="unspecified")
    gender = models.TextField(default="unspecified")
    autistic_identification = models.TextField(default="unspecified")
    description = models.TextField(default="")
    location = models.TextField(default="")
    comms_review = models.BooleanField(default=False)

    abuse = models.BooleanField(default=False)
    violence = models.BooleanField(default=False)
    drug = models.BooleanField(default=False)
    mentalhealth = models.BooleanField(default=False)
    negbody = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    def __str__(self):
        return "Profile for {}".format(self.user.username)


