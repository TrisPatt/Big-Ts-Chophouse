from django import forms
from .models import reservation

class reservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['user_id', 'date', 'time', 'num_of_guests', 'allergies', 'special_reqs']
