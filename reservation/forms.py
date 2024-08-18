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


    def available_time_slots(request):
        selected_date = request.GET.get('date', date.today())
        all_time_slots = TimeSlot.objects.all()
        booked_slots = Booking.objects.filter(date=selected_date).values('time').annotate(total_guests=models.Sum('number_of_guests')).filter(total_guests__gte=24)
        available_slots = all_time_slots.exclude(id__in=[slot['time'] for slot in booked_slots])

        return render(request, 'available_time_slots.html', {'available_slots': available_slots})


    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests', 'first_name', 'last_name', 'email', 'allergies','special_requirements']


    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time')
        number_of_guests = cleaned_data.get('number_of_guests')

        time = None

        if date and time_slot:
            time = time_slot.time
            reservation_datetime = datetime.combine(date, time)
            now = datetime.now()

            if reservation_datetime < now:
                raise forms.ValidationError("Reservation cannot be in the past.")

        return cleaned_data

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