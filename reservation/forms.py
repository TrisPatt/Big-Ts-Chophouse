from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'})
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker2'})
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'allergies', 'special_requirements']