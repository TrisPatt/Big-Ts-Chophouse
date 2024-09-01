from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, timedelta
from .forms import ReservationForm
from .models import Reservation, TimeSlot


class TestReservationForm(TestCase):
    """
    Test cases for the ReservationForm.

    This class contains tests that verify the correct behavior of 
    the ReservationForm, including form initialization, validation 
    of dates, guest capacity, and required fields.
    """
    def setUp(self):
        """Initialize common data for all tests."""
        self.user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        self.timeslot = TimeSlot.objects.create(time="12:00:00")
        self.future_date = (datetime.now() + timedelta(days=1)).date()
        self.past_date = (datetime.now() - timedelta(days=1)).date()
        self.form_data = {
            'date': self.future_date,
            'time': self.timeslot.id,
            'number_of_guests': 4,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }

    def test_form_initialization_with_date(self):
        """
        Test that the form is correctly initialized with a date.

        This test ensures that when the form is initialized with a date, the
        queryset for the 'time' field is populated with TimeSlot objects.
        """
        form = ReservationForm(data={'date': self.future_date})
        self.assertTrue(
            form.fields['time'].queryset.exists(),
            """Expected time queryset to be populated with 
            TimeSlot objects, but it was empty."""
        )

    def test_form_initialization_with_user(self):
        """
        Test that the form is correctly initialized with a user.

        This test ensures that when the form is initialized with a user, the
        'first_name', 'last_name', and 'email' fields are pre-filled with the
        user's corresponding information.
        """
        form = ReservationForm(user=self.user)
        
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
        """
        Test that the form is invalid if the reservation date is in the past.

        This test ensures that the form cannot be submitted with a reservation
        date that is in the past, and that the appropriate error message is displayed.
        """
        form_data = self.form_data.copy()
        form_data['date'] = self.past_date
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

    def test_clean_method(self):
        """
        Test the clean method of the form with valid data.

        This test ensures that the form is valid when all required fields are
        filled with valid data, including a future reservation date and 
        available guest slots.
        """
        form = ReservationForm(data= self.form_data)

        self.assertTrue(
            form.is_valid(),
            """Form should be valid with future date, 
            available time slot, and valid guest number."""
        )

    def test_missing_required_fields(self):
        """
        Test that the form is invalid when required fields are missing.

        This test ensures that the form is not valid if 'date', 'time', or
        'number_of_guests' fields are missing, and that appropriate error 
        messages are displayed.
        """
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
        """Test that the form is valid when guest number equals max capacity."""
        form_data = self.form_data.copy()
        form_data['number_of_guests'] = 24
        form = ReservationForm(data=form_data)

        self.assertTrue(
            form.is_valid(),
            """Form should be valid when the number of guests 
            equals the maximum capacity."""
        )

    def test_zero_no_number_of_guests(self):
        """Test that form is invalid if 0 guests are entered"""
        form_data = self.form_data.copy()
        form_data['number_of_guests'] = 0
        form = ReservationForm(data=form_data)

        self.assertFalse(
            form.is_valid(),
            """Form should be invalid if 0 guests are entered"""
        )
        self.assertIn('number_of_guests', form.errors)

def test_exceeding_guest_limit(self):
    """Test that form is invalid if guest capacity exceeds 24"""
    Reservation.objects.create(
        date=self.date_tomorrow,
        time=self.time_slot, 
        number_of_guests=20,
        reservation_status=0
    )

    form_data = {
        'date': self.date_tomorrow,
        'time': self.time_slot.id, 
        'number_of_guests': 10,
    }

    form = ReservationForm(data=form_data)
    self.assertFalse(
        form.is_valid(), 
        """Form should be invalid if guest capacity exceeds 24"""
    )
    with self.assertRaises(ValidationError):
        form.clean()
