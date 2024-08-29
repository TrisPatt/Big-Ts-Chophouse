from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    """
    A form for updating the User model's basic information.

    This form includes fields for first name, last name, and email,
    which are all attributes of the built-in Django User model.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    """
    A form for updating the Profile model's additional user information.

    This form includes fields for phone number and date of birth,
    which are attributes of the custom Profile model.
    """
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth']


class CombinedUserProfileForm(forms.Form):
    """
    A form for updating both User and Profile model data simultaneously.

    This form combines fields from both the User model (first name, last name,
    email)
    and the Profile model (phone number, date of birth) into a single form.

    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    phone_number = forms.CharField(max_length=30, required=False)
    date_of_birth = forms.DateField(
        required=False, help_text='(Format: yyyy-mm-dd)')

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with user and profile instances.

        If instances of User and Profile are provided, the form fields
        are pre-populated with their respective data.
        """
        self.user = kwargs.pop('user', None)
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

        if self.user and self.profile:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.profile.phone_number
            self.fields['date_of_birth'].initial = self.profile.date_of_birth

    def save(self):
        """
        Saves the form data to both User and Profile models.

        The user-related data is saved to the User model, and the
        profile-related data is saved to the Profile model.
        """
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()

        if self.profile:
            self.profile.phone_number = self.cleaned_data['phone_number']
            self.profile.date_of_birth = self.cleaned_data['date_of_birth']
            self.profile.save()
            
