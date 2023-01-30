from django import forms

class ShareExperienceForm(forms.Form):
        
    experience = forms.CharField(label='Please share your story', max_length=500, strip=True,
                                 widget=forms.Textarea(attrs={'placeholder':'Write your story here',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    experience.group = 1
    wish_different = forms.CharField(label='Suggestions for what could have made your story better',
                                     strip=True, max_length=500,
                                     widget=forms.Textarea(attrs={'placeholder':'Write your story here',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    wish_different.group = 1
    title = forms.CharField(label='Choose a title for your story', 
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(attrs={'placeholder':'Title',
                                                          'class':'form-control'}))
    title.group = 1
    
    
    
    # add triggering here
    abuse = forms.BooleanField(label = 'Abuse (physical, sexual, emotional and verbal)', required=False)
    abuse.group = 2
    violence = forms.BooleanField(label = 'Violence and Assault', required=False)
    violence.group = 2
    drug = forms.BooleanField(label = 'Drug and/or Alcohol misuse', required=False)
    drug.group = 2
    mentalhealth = forms.BooleanField(label = 'Mental Health Issues', required=False)
    mentalhealth.group = 2
    negbody = forms.BooleanField(label = 'Negative body image', required=False)
    negbody.group = 2
    
    other = forms.CharField(label='Other',
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(), required=False)
    other.group = 2
    
    # sharing options
    viewable = forms.BooleanField(label = "Share on AutSPACE website", required=False)
    viewable.group = 3
    research = forms.BooleanField(label = "Share for research", required=False)
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
    
    def __init__(self, *args, **kwargs):
        """ Disable free text fields to the moderator, or disable all fields if in 'read only' mode"""
        
        disable_all = kwargs.pop('disable_all', False) #disable everything
        disable_moderator = kwargs.pop('disable_moderator', False) # only the free text fields
        
        super(ShareExperienceForm, self).__init__(*args, **kwargs)

                
        for field in self.fields:
            if field in ['experience','wish_different','title','research','viewable']: 
                self.fields[field].widget.attrs['disabled']= disable_moderator or disable_all
            else:
                self.fields[field].widget.attrs['disabled']= disable_all
                
    
    def clean_moderation_status(self):
        mod_status = self.cleaned_data['moderation_status']
        if not mod_status:
            mod_status = 'not reviewed'
            
        return mod_status
            