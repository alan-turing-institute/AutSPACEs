from django.db import models
from openhumans.models import OpenHumansMember


class PublicExperience(models.Model):
    experience_text = models.TextField()
    difference_text = models.TextField(default="")
    title_text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)
    experience_id = models.TextField(primary_key=True) #if specified as primary key you cannot have duplicates.
    open_humans_member = models.ForeignKey(OpenHumansMember,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)
    approved = models.CharField(
        blank=False,
        default='not reviewed',
        max_length=50)
    
    abuse = models.BooleanField(default=False)
    violence = models.BooleanField(default=False)
    drug = models.BooleanField(default=False)
    mentalhealth = models.BooleanField(default=False)
    negbody = models.BooleanField(default=False)
    other = models.TextField(default="")
    
    research = models.BooleanField(default=False)

    def __str__(self):
        return self.experience_text
