from django import forms
from .models import Reservation, Table, TimeSlot
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q
from django.utils import timezone


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'reservation-date',
            'data-provide': 'datepicker',  
            'data-date-format': 'yyyy-mm-dd',
            'min': timezone.now().date().strftime('%y-%m-%d'),
        })
    )

    time = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the 'time' field's queryset
        self.fields['time'].queryset = TimeSlot.objects.all()

        if 'date' in self.data:
            try:
                date_str = self.data.get('date')
                if date_str:
                    # Parse the date string to a date object
                    date_obj = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

                    # Annotate each TimeSlot with the total number of guests booked on the selected date
                    available_time_slots = TimeSlot.objects.annotate(
                        total_guests=Sum(
                            'reservation__number_of_guests',
                            filter=Q(reservation__date=date_obj) & Q(reservation__reservation_status=0)
                        )
                    ).filter(
                        Q(total_guests__lt=24) | Q(total_guests__isnull=True)  # Include time slots with less than 24 guests or no reservations
                    )

                    self.fields['time'].queryset = available_time_slots
                else:
                    self.fields['time'].queryset = TimeSlot.objects.none()
            except (ValueError, TypeError):
                self.fields['time'].queryset = TimeSlot.objects.none()
        else:
            # For initial form rendering, display all time slots
            self.fields['time'].queryset = TimeSlot.objects.all()

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'allergies','special_requirements']


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
                raise ValidationError('Unfortunately we are fully booked at this time.')

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
