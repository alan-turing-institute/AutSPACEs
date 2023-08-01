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
    moderation_status = models.CharField(
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

    experience_authorship = models.CharField(
        blank=False,
        default='AutSPACEs contributor',
        max_length=100)
    
    author_relationship = models.CharField(
        default = " ",
        max_length = 150,
    )

    def __str__(self):
        return self.experience_text

class ExperienceHistory(models.Model):
    experience = models.ForeignKey(PublicExperience, on_delete=models.CASCADE)
    change_type = models.TextField()
    changed_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(OpenHumansMember, 
                                   blank=False,
                                   null=False,
                                   on_delete=models.CASCADE)
    change_comments = models.TextField(default="")
    change_reply = models.TextField(default="")

    def __str__(self):
        return self.change_type