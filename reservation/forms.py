from django import forms
from .models import reservation

class reservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['date', 'time', 'number_of_guests', 'allergies', 'special_requirements']
