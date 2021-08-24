from django.db import models
from openhumans.models import OpenHumansMember


class Experience(models.Model):
    experience = models.TextField()
    suggestion = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)
    experience_id = models.TextField()
    permission = models.TextField()
    open_humans_member = models.ForeignKey(OpenHumansMember,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    approved = models.CharField(
        blank=False,
        default='draft',
        max_length=50)
