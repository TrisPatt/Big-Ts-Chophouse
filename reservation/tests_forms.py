from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .forms import ReservationForm
from .models import Reservation, TimeSlot


class TestReservationForm(TestCase):
    
    def test_form_initialization_with_date(self):
        timeslot = TimeSlot.objects.create(time="12:00:00")
        data = {'date': '2024-12-01'}
        form = ReservationForm(data=data)

        self.assertTrue(
            form.fields['time'].queryset.exists(),
            """Expected time queryset to be populated with 
            TimeSlot objects, but it was empty."""
        )

    def test_form_initialization_with_user(self):
        user = User.objects.create_user(
            username='testuser', 
            first_name='John', 
            last_name='Doe', 
            email='john@example.com'
            )
        form = ReservationForm(user=user)
        
        self.assertEqual(
            form.fields['first_name'].initial, 'John',
            "Expected first name to be 'John' but got something else."
        )
        self.assertEqual(
            form.fields['last_name'].initial, 'Doe',
            "Expected last name to be 'Doe' but got something else."
        )
        self.assertEqual(
            form.fields['email'].initial, 'john@example.com',
            "Expected email to be 'john@example.com' but got something else."
        )

    def test_reservation_in_past(self):
        timeslot = TimeSlot.objects.create(time="12:00:00")
        past_date = (datetime.now() - timedelta(days=1)).date()
        form_data = {
            'date': past_date,
            'time': timeslot.id,
            'number_of_guests': 4,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        form = ReservationForm(data=form_data)

        self.assertFalse(
            form.is_valid(),
            "Form should be invalid when reservation date is in the past."
        )
        self.assertIn(
            "Reservation cannot be in the past.", form.errors['__all__'],
            """Expected 'Reservation cannot be in the past.' error message, 
            but it was not found."""
        )

    def test_guest_capacity_exceeded(self):
        timeslot = TimeSlot.objects.create(time="12:00:00")
        date = datetime.now().date()

        Reservation.objects.create(
            date=date, time=timeslot, number_of_guests=22, reservation_status=0
            )

        form_data = {
            'date': date,
            'time': timeslot.id,
            'number_of_guests': 4,  
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        form = ReservationForm(data=form_data)

        self.assertFalse(
            form.is_valid(),
            """Form should be invalid when the number of guests 
            exceeds the maximum capacity."""
        )
        self.assertIn(
            "Only 2 guest slots are available.", form.errors['__all__'],
            """Expected 'Only 4 guest slots are available.' 
            error message, but it was not found."""
        )

    def test_clean_method(self):
        timeslot = TimeSlot.objects.create(time="12:00:00")
        date = (datetime.now() + timedelta(days=1)).date()  

        form_data = {
            'date': date,
            'time': timeslot.id,
            'number_of_guests': 4,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        form = ReservationForm(data=form_data)

        self.assertTrue(
            form.is_valid(),
            """Form should be valid with future date, 
            available time slot, and valid guest number."""
        )

    def test_missing_required_fields(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        form = ReservationForm(data=form_data)

        self.assertFalse(
            form.is_valid(),
            """Form should be invalid when required fields like 'date', 
            'time', or 'number_of_guests' are missing."""
        )
        self.assertIn(
            'date', form.errors,
            "Expected 'date' field to have an error, but it was not found."
        )
        self.assertIn(
            'time', form.errors,
            "Expected 'time' field to have an error, but it was not found."
        )
        self.assertIn(
            'number_of_guests', form.errors,
            """Expected 'number_of_guests' field to have an error, 
            but it was not found."""
        )

    def test_maximum_guest_capacity(self):
        timeslot = TimeSlot.objects.create(time="12:00:00")
        date = datetime.now().date()

        form_data = {
            'date': date,
            'time': timeslot.id,
            'number_of_guests': 24,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        form = ReservationForm(data=form_data)

        self.assertTrue(
            form.is_valid(),
            """Form should be valid when the number of guests 
            equals the maximum capacity."""
        )

