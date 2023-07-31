from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Holds profile information about a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_submitted = models.BooleanField(default=False)
    autistic_identification = models.TextField(default="")
    age_bracket = models.TextField(default="unspecified")
    age_public = models.BooleanField(default=False)
    gender = models.TextField(default="unspecified")
    gender_self_identification = models.TextField(default="")
    gender_public = models.BooleanField(default=False)
    description = models.TextField(default="")
    description_public = models.BooleanField(default=False)
    comms_review = models.BooleanField(default=False)

    abuse = models.BooleanField(default=False)
    violence = models.BooleanField(default=False)
    drug = models.BooleanField(default=False)
    mentalhealth = models.BooleanField(default=False)
    negbody = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    def __str__(self):
        return "Profile for {}".format(self.user.username)


