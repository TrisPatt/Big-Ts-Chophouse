from django import forms
from .models import Reservation, Table
from django.core.exceptions import ValidationError
from django.db.models import Sum

class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'reservation-date',
            'data-target': '#datetimepicker1'
        })
    )
    time = forms.ChoiceField(
        choices=[],  # Choices will be populated dynamically
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'allergies', 'special_requirements']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].choices = self.get_available_times()

    def get_available_times(self):
        """
        Returns a list of available time slots based on the restaurant's operating hours.
        """
        date = self.initial.get('date')
        if date:
            day_of_week = date.strftime('%A').lower()
            opening_hours = settings.RESTAURANT_OPENING_HOURS.get(day_of_week)
            if opening_hours:
                open_time = datetime.strptime(opening_hours[0], '%H:%M')
                close_time = datetime.strptime(opening_hours[1], '%H:%M')
                time_slots = [(f"{(open_time + timedelta(minutes=30*i)).strftime('%H:%M')}", f"{(open_time + timedelta(minutes=30*i)).strftime('%H:%M')}") for i in range((close_time - open_time).seconds // 1800 + 1)]
                return time_slots
        return []

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')

        
        if date and time and number_of_guests:
            total_guests = Reservation.objects.filter(date=date, time=time, reservation_status=0 ).aggregate(total_guests=Sum('number_of_guests'))['total_guests'] or 0
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
