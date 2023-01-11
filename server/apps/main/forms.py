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
    
    
    # hidden field that tracks PublicExperience uuid (which is also the OH filename) when you're editing an experience
    uuid = forms.CharField(required=False, widget=forms.HiddenInput())
    uuid.group = "hidden"
    # hidden field for moderation status
    moderation_status = forms.BooleanField(widget = forms.HiddenInput(), required=False, initial=False)
    moderation_status.group = "hidden"
    
