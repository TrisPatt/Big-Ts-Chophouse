from django import forms
from .models import Reservation, Table, TimeSlot
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'reservation-date',
            'type': 'text',           
        })
    )
    time = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Initialize the 'time' field's queryset
        self.fields['time'].queryset = TimeSlot.objects.all()

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email


    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'first_name', 'last_name', 'email', 'allergies','special_requirements']


    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')

        if not date or not time_slot or not number_of_guests:
            return cleaned_data  # Skip validation if required fields are missing

        # Get the time from the TimeSlot object
        time = time_slot.time


        reservation_datetime = datetime.combine(date, time)
        now = datetime.now()
        if reservation_datetime < now:
            raise ValidationError("Reservation cannot be in the past.")

            if reservation_datetime < now:
                raise forms.ValidationError("Reservation cannot be in the past.")

        return cleaned_data

        # Check if the total number of guests exceeds 24 for the selected time
        total_guests = Reservation.objects.filter(
            date=date,
            time=time,
            reservation_status=0  
        ).aggregate(total_guests=Sum('number_of_guests'))['total_guests'] or 0

        if total_guests + number_of_guests > 24:
            remaining_capacity = 24 - total_guests
            raise ValidationError(
                f"Sorry, we cannot accommodate {number_of_guests} guests at the requested time. "
                f"Only {remaining_capacity} guest slots are available."
            )

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