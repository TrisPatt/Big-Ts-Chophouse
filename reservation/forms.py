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

#cancel reervation
class CancelReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_status']             

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_status'].initial = 1  # Set initial value to "cancelled"
        self.fields['reservation_status'].widget = forms.HiddenInput()  # Hide the field from the form
