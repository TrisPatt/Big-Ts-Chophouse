from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth']


class CombinedUserProfileForm(forms.Form):
    # Fields from User model
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    # Fields from Profile model
    phone_number = forms.CharField(max_length=30, required=False)
    date_of_birth = forms.DateField(required=False, help_text='Format: yyyy/mm/dd')
    
    def __init__(self, *args, **kwargs):
        # Instance of the User and Profile objects
        self.user = kwargs.pop('user', None)
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.profile:
            # Populate form fields with existing data
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.profile.phone_number
            self.fields['date_of_birth'].initial = self.profile.date_of_birth

    def save(self):
        # Save the user data
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        
        # Save the profile data
        if self.profile:
            self.profile.phone_number = self.cleaned_data['phone_number']
            self.profile.date_of_birth = self.cleaned_data['date_of_birth']
            self.profile.save()
