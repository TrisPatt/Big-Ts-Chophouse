from django import forms
from .models import Reservation, Table, TimeSlot
from django.core.exceptions import ValidationError
from django.db.models import Sum

class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'reservation-date',
            'data-provide': 'datepicker',  
            'data-date-format': 'dd-mm-yyyy'
        })
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time_slot', 'number_of_guests', 'allergies', 'special_requirements']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date' in self.data:
            try:
                selected_date = self.data.get('date')
                selected_date = datetime.datetime.strptime(selected_date, '%d-%m-%Y').date()
                weekday = selected_date.strftime('%A')
                self.fields['time_slot'].queryset = TimeSlot.objects.filter(weekday=weekday)
            except (ValueError, TypeError):
                pass

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise ValidationError("The date cannot be in the past.")
        return date

    
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
