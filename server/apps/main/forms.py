from django import forms

class ShareExperienceForm(forms.Form):
    experience = forms.CharField(label='Please share your story', max_length=500, strip=True,
                                 widget=forms.Textarea(attrs={'placeholder':'Write your story here',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    
    wish_different = forms.CharField(label='Suggestions for what could have made your story better',
                                     strip=True, max_length=500,
                                     widget=forms.Textarea(attrs={'placeholder':'Write your story here',
                                                              'rows':'4',
                                                              'class':'form-control'}))
    
    title = forms.CharField(label='Choose a title for your story', 
                            strip=True,
                            max_length=150,
                            widget=forms.TextInput(attrs={'placeholder':'Title',
                                                          'class':'form-control'}))
    
    
    
    
    # add triggering here
    abuse = forms.BooleanField(label = 'Abuse (physical, sexual, emotional and verbal)', required=False)
    violence = forms.BooleanField(label = 'Violence and Assualt', required=False)
    drug = forms.BooleanField(label = 'Drug and/or Alcohol misuse', required=False)
    mentalhealth = forms.BooleanField(label = 'Mental Health Issues', required=False)
    negbody = forms.BooleanField(label = 'Negative body image', required=False)
    other = forms.CharField(label='',
                            max_length=150,
                            widget=forms.TextInput(attrs={'placeholder':'Other'}), required=False)
    
    
    
    
    # sharing options
    viewable = forms.BooleanField(label = "Share on AutSPACE website", required=False)
    research = forms.BooleanField(label = "Share for research", required=False)
    
    
    # grouping for different treatment in share_experience.
    for f in [experience, wish_different, title]: f.group = 1
    for f in [abuse,violence, drug, mentalhealth,negbody,other]: f.group = 2
    for f in [viewable, research]: f.group = 3