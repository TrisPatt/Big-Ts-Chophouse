from django import forms
from .models import Reservation, Table
from django.core.exceptions import ValidationError
from django.db.models import Sum

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

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')

        if date and time and number_of_guests:
            total_guests = Reservation.objects.filter(date=date, time=time).aggregate(total_guests=Sum('number_of_guests'))['total_guests'] or 0
            if total_guests + number_of_guests > 24:
                raise ValidationError('Cannot make reservation. Exceeds maximum capacity.')

        return cleaned_data


#cancel reervation
class CancelReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_status']             

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_status'].initial = 1  # Set initial value to "cancelled"
        self.fields['reservation_status'].widget = forms.HiddenInput()  # Hide the field from the form
