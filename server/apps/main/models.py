from django.db import models
from openhumans.models import OpenHumansMember


class PublicExperience(models.Model):
    experience_text = models.TextField()
    difference_text = models.TextField(default="")
    title_text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)
    experience_id = models.TextField()
    open_humans_member = models.ForeignKey(OpenHumansMember,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    approved = models.CharField(
        blank=False,
        default='not reviewed',
        max_length=50)
