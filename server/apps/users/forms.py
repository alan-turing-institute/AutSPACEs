from django import forms

class UserProfileForm(forms.Form):

    age_brackets = [
        ("under 18", "Under 18"),
        ("18-25", "18-25"),
        ("26-35", "26-35"),
        ("36-45", "36-45"),
        ("46-65", "46-65"),
        ("over 65", "Over 65"),
        ("unspecified", "Prefer not to say"),
    ]
    age_bracket = forms.ChoiceField(choices = age_brackets, widget = forms.Select(), required=False,
                                   label="What is your age?",
                                   initial="unspecified")
    age_bracket.group = 1

    genders = [
        ("nonbinary", "Non-binary"),
        ("female", "Female"),
        ("male", "Male"),
        ("see_description", "See description"),
        ("unspecified", "Prefer not to say"),
    ]
    gender = forms.ChoiceField(choices = genders, widget = forms.Select(), required=False,
                              label="Which gender do you identify as?",
                              initial="unspecified")
    gender.group = 1

    # Not intended as final
    autistic_identifications = [
        ("yes", "Yes"),
        ("no", "No"),
        ("not_sure", "Not sure"),
        ("self_describe", "Prefer to self-describe"),
        ("unspecified", "Prefer not to say"),
    ]
    autistic_identification = forms.ChoiceField(choices = autistic_identifications, widget = forms.Select(),
                                           label="Do you identify as autistic?",
                                           required=False, initial="unspecified")
    autistic_identification.group = 1

    description = forms.CharField(label="Description", max_length=2048, strip=True, required=False,
                                 widget=forms.Textarea(attrs={"placeholder":"An optional description of yourself",
                                                              "rows":"4",
                                                              "class":"form-control"}))
    description.group = 1

    location = forms.CharField(label="Location", max_length=500, initial="Earth", strip=True,
                              required=False,
                              widget=forms.TextInput(attrs={"placeholder":"Where do you live (town/city)",
                                                              "rows":"1",
                                                              "class":"form-control"}))
    location.group = 1

    # Add triggering here
    abuse = forms.BooleanField(label = "Abuse (physical, sexual, emotional and verbal)",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    abuse.group = 2
    violence = forms.BooleanField(label = "Violence and Assault",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    violence.group = 2
    drug = forms.BooleanField(label = "Drug and/or Alcohol misuse",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    drug.group = 2
    mentalhealth = forms.BooleanField(label = "Mental Health Issues",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    mentalhealth.group = 2
    negbody = forms.BooleanField(label = "Negative body image",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    negbody.group = 2
    other = forms.BooleanField(label = "Other",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    other.group = 2

    # Communications preferences
    comms_review = forms.BooleanField(label = "When the review status of your story changes",
        required = False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    comms_review.group = 3

    # New user management
    profile_submitted = forms.BooleanField(label = "Profile submitted",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))
    profile_submitted.group = "hidden"

