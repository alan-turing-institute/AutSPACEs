import json

from django import forms
from django.core.exceptions import ValidationError

class ShareExperienceForm(forms.Form):


    experience_text = forms.CharField(label='Please share your experience', strip=True,
                                help_text='Write your experience here. You can take as much or as little space as you need.',
                                widget=forms.Textarea(attrs={'placeholder':'Please share your story.',
                                                             'rows':'4',
                                                             'class':'form-control'}))
    experience_text.group = 1
    difference_text = forms.CharField(label='What could have made your experience better?',
                                      strip=True,
                                      help_text='Do you have anything that you would want to have changed to make it better? Or do you have any tips for others who may experience the same thing?',
                                      widget=forms.Textarea(attrs={'placeholder':'What could have been different?',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    difference_text.group = 1
    title_text = forms.CharField(label='Choose a title for your story', 
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(attrs={'placeholder':'Title',
                                                          'class':'form-control'}))
    title_text.group = 1
    
    
    
    # add triggering here
    abuse = forms.BooleanField(label = 'Abuse (physical, sexual, emotional and verbal)', required=False)
    abuse.group = 2
    violence = forms.BooleanField(label = 'Violence and assault', required=False)
    violence.group = 2
    drug = forms.BooleanField(label = 'Drug and/or alcohol misuse', required=False)
    drug.group = 2
    mentalhealth = forms.BooleanField(label = 'Mental health issues', required=False)
    mentalhealth.group = 2
    negbody = forms.BooleanField(label = 'Negative body image', required=False)
    negbody.group = 2

    other = forms.CharField(label='Other',
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(), required=False)
    other.group = 2

    # sharing options
    viewable = forms.BooleanField(label = "Share publicly on AutSPACE website", 
                                  required=False,
                                  widget=forms.CheckboxInput(attrs={'id':'shareOnAutSPACEs'}))
    viewable.group = 3
    research = forms.BooleanField(label = "Allow story to be used for research", required=False)
    research.group = 3

    # hidden field for moderation status
    statuses = [
        ("not reviewed", "not reviewed"),
        ("in review", "in review"),
        ("approved", "approved"),
        ("rejected", "rejected"),
    ]
    moderation_status = forms.ChoiceField(choices = statuses, widget = forms.Select(), required=False)
    moderation_status.group = "hidden"

    authorship_choices = [
        (True, "Experience is my own"),
        (False, "Experience is someone else's"),
    ]
    first_hand_authorship = forms.ChoiceField(choices = authorship_choices, widget = forms.RadioSelect(), required=True)
    first_hand_authorship.group = 4

    authorship_relation = forms.CharField(label="Relationship",
                                 max_length=300, strip=True, required=False,
                                 widget=forms.TextInput(),
                                 help_text='For example: "I am the non-autistic parent of an autistic adult", "I am the autistic parent of autistic children", "I am a teacher who works with autistic people", "I am best friends of an autistic person". - Please do not share personally identifying information.')
    authorship_relation.layout_horizontal = True
    authorship_relation.group = 4


    def clean(self):
        # Raise an error if second-hand authorship chosen with no description
        # Raise an error if first-hand authorship has a relationship description

        cleaned_data = super().clean()

        first_hand_authorship = cleaned_data.get("first_hand_authorship")
        authorship_relation = cleaned_data.get("authorship_relation")

        if first_hand_authorship == "False" and authorship_relation == "":
                self.add_error("first_hand_authorship", ValidationError(("Stories written on behalf of someone else must have a description of the relationship"), code="invalid"))
        if first_hand_authorship == "True" and authorship_relation != "":
                self.add_error("first_hand_authorship", ValidationError(("First hand stories do not require a relationship field"), code="invalid"))

    def __init__(self, *args, **kwargs):
        """ Disable free text fields to the moderator, or disable all fields if in 'read only' mode"""

        disable_all = kwargs.pop('disable_all', False) #disable everything
        disable_moderator = kwargs.pop('disable_moderator', False) # only the free text fields

        super(ShareExperienceForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            if field in ['experience_text','difference_text','title_text','research','viewable']: 
                self.fields[field].widget.attrs['disabled']= disable_moderator or disable_all
            else:
                self.fields[field].widget.attrs['disabled']= disable_all


    def clean_moderation_status(self):
        mod_status = self.cleaned_data['moderation_status']
        if not mod_status:
            mod_status = 'not reviewed'

        return mod_status
    



class ModerateExperienceForm(forms.Form):
        
    # trigger labels
    abuse = forms.BooleanField(label = 'Abuse (physical, sexual, emotional and verbal)', required=False)
    abuse.group = 2
    violence = forms.BooleanField(label = 'Violence and assault', required=False)
    violence.group = 2
    drug = forms.BooleanField(label = 'Drug and/or alcohol misuse', required=False)
    drug.group = 2
    mentalhealth = forms.BooleanField(label = 'Mental health issues', required=False)
    mentalhealth.group = 2
    negbody = forms.BooleanField(label = 'Negative body image', required=False)
    negbody.group = 2

    other = forms.CharField(label='Other',
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(), required=False)
    other.group = 2

    # moderation options 
    statuses = [
        ("not reviewed", "not reviewed"),
        ("in review", "in review"),
        ("approved", "approved"),
        ("rejected", "rejected"),
    ]
    moderation_status = forms.ChoiceField(choices = statuses, widget = forms.Select(), required=False)
    moderation_status.group = "hidden"

    moderation_comments = forms.CharField(label='Moderation comment', max_length=500, strip=True, required=False,
                                 widget=forms.Textarea(attrs={'placeholder':'These comments will only be visible to other moderators',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    moderation_comments.group = 4

    moderation_reply = forms.CharField(widget=forms.HiddenInput(), strip=True, required=False)
    moderation_reply.group = "hidden"

    moderation_prior = forms.CharField(widget=forms.HiddenInput())
    moderation_prior.group = "hidden"

    authorship_choices = [
        (True, "Experience is my own"),
        (False, "Experience is someone else's"),
    ]
    first_hand_authorship = forms.ChoiceField(choices = authorship_choices, widget = forms.RadioSelect(), required=True)
    first_hand_authorship.group = 5

    authorship_relation = forms.CharField(label="Relationship",
                                 max_length=300, strip=True, required=False,
                                 widget=forms.TextInput(),
                                 help_text='For example: "I am the non-autistic parent of an autistic adult", "I am the autistic parent of autistic children", "I am a teacher who works with autistic people", "I am best friends of an autistic person". - Please do not share personally identifying information.')
    authorship_relation.group = 5

    def __init__(self, *args, **kwargs):
        """ Disable free text fields to the moderator, or disable all fields if in 'read only' mode"""

        disable_all = kwargs.pop('disable_all', False) #disable everything
        disable_moderator = kwargs.pop('disable_moderator', False) # only the free text fields

        super(ModerateExperienceForm, self).__init__(*args, **kwargs)


        for field in self.fields:
            if field in ['experience_text','difference_text','title_text','research','viewable']: 
                self.fields[field].widget.attrs['disabled']= disable_moderator or disable_all
            else:
                self.fields[field].widget.attrs['disabled']= disable_all


    def clean_moderation_status(self):
        mod_status = self.cleaned_data['moderation_status']
        if not mod_status:
            mod_status = 'not reviewed'

        return mod_status

    def clean_moderation_reply(self):
        moderation_reply = self.cleaned_data['moderation_reply']
        if moderation_reply == '[]' or moderation_reply == '{}':
            moderation_reply = ""

        return moderation_reply

    def clean(self):
        # Raise an error if status is "not reviewed" and moderation_comments isn't empty
        cleaned_data = super().clean()
        moderation_status = cleaned_data.get("moderation_status")
        moderation_reply = cleaned_data.get("moderation_reply")
        if moderation_status == "not reviewed" and moderation_reply:
            raise ValidationError(
                "Stories that are not being reviewed cannot have moderation replies added to them."
            )
        # Raise an error if status is "approved" and there are "Red" severity moderation comments
        if moderation_status == "approved":
            try:
                reasons = json.loads(moderation_reply)
                red_reasons = sum(map(lambda x : 1 if x.get('severity', None) == 'red' else 0, reasons))
            except:
                red_reasons = 0
            if red_reasons > 0:
                raise ValidationError(
                    "Stories with Red moderation reasons can't be given approved status."
                )

