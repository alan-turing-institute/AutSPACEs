from django import forms

class SelectRequired(forms.Select):
    # Disables items in the drop down list that have an empty value
    # See https://docs.djangoproject.com/en/4.2/ref/forms/renderers/#built-in-template-form-renderers
    # See also the ChoiceWidget.create_option() implementation in django/forms/widgets.py
    option_template_name = "users/select_option_disable_empty.html"

class UserProfileForm(forms.Form):

    autistic_identifications = [
        ("", "Please select"),
        ("yes", "Yes"),
        ("no", "No"),
        ("unspecified", "Prefer not to say"),
    ]
    
    autistic_identification = forms.ChoiceField(choices = autistic_identifications, widget = SelectRequired(attrs={
        "class": "form-select",
        "aria-describedby": "help_id_autistic_identification"}
        ),
                                           label="Do you identify as autistic?",
                                           help_text="AutSPACEs is focused on collecting and sharing the voices and lived experiences of autistic people, which is why we <strong>require a conscious decision for this question</strong>. If you select <i>prefer not to say</i> your experiences will be considered as coming from a non-autistic person, labeled as such and e.g. not used for research.",
                                           required=True,
                                           initial="")
    autistic_identification.group = 1

    age_brackets = [
        ("18-25", "18-25"),
        ("26-35", "26-35"),
        ("36-45", "36-45"),
        ("46-65", "46-65"),
        ("over 65", "Over 65"),
        ("unspecified", "Prefer not to say"),
    ]
    age_bracket = forms.ChoiceField(choices = age_brackets, widget = forms.Select(attrs={
        "class": "form-select",
        "aria-describedby": "help_id_age_bracket"}
        ), 
                                   required=False,
                                   label="What is your age group?",
                                   help_text="Sharing your age might help researchers understand potential trends across age groups. It can also help readers to better understand your perspective if this data is made public.",
                                   initial="unspecified")
    age_bracket.group = 1

    age_public = forms.BooleanField(label = "Make age public",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    age_public.group = 1
    age_public.gap = True

    genders = [
        ("nonbinary", "Non-binary"),
        ("female", "Female"),
        ("male", "Male"),
        ("self_identify", "Self identify"),
        ("unspecified", "Prefer not to say"),
    ]
    gender = forms.ChoiceField(choices = genders, widget = forms.Select(attrs={
        "class": "form-select",
        "aria-describedby": "help_id_gender"}
        ), 
                              required=False,
                              label="What gender do you identify with?",
                              help_text="Sharing your gender identity might help researchers understand potential trends across different demographics. It can also help readers to better understand your perspective if this data is made public. You can also choose to self-identify instead of using one of the pre-given options.",
                              initial="unspecified")
    gender.group = 1


    gender_self_identification = forms.CharField(label="Self identification",
                                 max_length=150, strip=True, required=False,
                                 widget=forms.TextInput())

    gender_self_identification.group = 1
    gender_self_identification.layout_horizontal = True

    gender_public = forms.BooleanField(label = "Make gender public",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))

    gender_public.group = 1
    gender_public.gap = True

    description = forms.CharField(label="What else would you like researchers (or readers) to know about yourself?",
                                 max_length=2048, strip=True, required=False,
                                 help_text="""You can provide any additional context about yourself here that you deem 
                                 relevant to understanding your perspective and experiences. This could be your ethnicity, 
                                 where you grew up, your educational background, or when and how you (self-)diagnosed.
                                 The AutSPACEs team might use this information to refine the structured demographic questions above. 
                                 You can also make this information publicly accessible &mdash; which might be linked to your public experiences in the future.""",
                                 widget=forms.Textarea(attrs={"placeholder":"Optionally share more about yourself",
                                                              "rows":"4",
                                                              "class":"form-control",
                                                              "aria-describedby": "help_id_description"}))
    description.group = 1

    description_public = forms.BooleanField(label = "Make description public",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    description_public.group = 1

    # Add triggering here
    abuse = forms.BooleanField(label = "Abuse (physical, sexual, emotional and verbal)",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    abuse.group = 2
    violence = forms.BooleanField(label = "Violence and assault",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    violence.group = 2
    drug = forms.BooleanField(label = "Drug and/or alcohol misuse",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    drug.group = 2
    mentalhealth = forms.BooleanField(label = "Mental health issues",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    mentalhealth.group = 2
    negbody = forms.BooleanField(label = "Negative body image",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    negbody.group = 2
    other = forms.BooleanField(label = "Other",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    other.group = 2

    # Communications preferences
    comms_review = forms.BooleanField(label = "Moderation reviews of my experiences",
        required = False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    comms_review.group = 3

    # New user management
    profile_submitted = forms.BooleanField(label = "Profile submitted",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input","type": "checkbox","role": "switch"}))
    profile_submitted.group = "hidden"

class UserProfileDeleteForm(forms.Form):
    delete_oh_data = forms.BooleanField(label = "Delete your stories from OpenHumans",
                                       required=False,
                                       widget=forms.CheckboxInput(attrs={
                                           "class": "form-check-input",
                                           "type": "checkbox",
                                           "role": "switch"
                                           }))
