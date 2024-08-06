from django import forms
from .models import reservation

class reservationForm(forms.ModelForm):
    class Meta:
        model = reservation
        fields = ['reservation_num', 'user_id', 'date', 'time', 'num_of_gusets', 'allergies', 'special_reqs', 'reservation_status', 'created_on']
