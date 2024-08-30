from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import TimeSlot


class TestReservationCreateView(TestCase):
    """
    Test cases for the reservation creation, update, and confirmation views.
    
    This class contains tests for both GET and POST requests to the reservation 
    creation and update views. It also tests the reservation list and confirmation 
    views, ensuring correct handling of authenticated and unauthenticated users.

    """
    def setUp(self):
        """
        Set up a test user and log them in for the tests.
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.client.login(username='testuser', password='12345')

    def test_get_reservation_create(self):
        """
        Test the GET request to the reservation creation view.
        
        This test checks that the reservation form is rendered correctly with 
        a status code of 200 and the correct template is used.
        """
        response = self.client.get(reverse('reservation_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'reservation/reservation_form.html'
            )

    def test_post_reservation_create_valid(self):
        """
        Test a valid POST request to the reservation creation view.
        
        This test submits a valid reservation form and checks that the user is 
        redirected to the confirmation page and the reservation is saved in 
        the database.
        """
        timeslot = TimeSlot.objects.create(time="12:00:00")
        form_data = {
            'date': '2024-09-01',
            'time': timeslot.id,
            'number_of_guests': 2,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com'
        }
        response = self.client.post(reverse('reservation_create'), data=form_data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Reservation.objects.filter(email='john@example.com').exists())

    def test_post_reservation_create_invalid(self):
        """
        Test an invalid POST request to the reservation creation view.
        
        This test submits an invalid reservation form and checks that the form 
        reloads with errors and does not create a reservation.
        """
        form_data = {
            'date': '',
            'time': '',
            'number_of_guests': ''
        }
        response = self.client.post(reverse('reservation_create'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'date', 'This field is required.')
        self.assertFormError(response, 'form', 'time', 'This field is required.')

    def test_get_update_reservation(self):
        """
        Test the GET request to the reservation update view.
        
        This test checks that the reservation update form is rendered correctly 
        with a status code of 200 and the correct template is used.
        """
        timeslot = TimeSlot.objects.create(time="12:00:00")
        reservation = Reservation.objects.create(
            user_id=self.user,
            date='2024-09-01', time=timeslot, number_of_guests=2, reservation_status=0)
        response = self.client.get(reverse('update_reservation', args=[reservation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_form.html')

    def test_post_update_reservation_valid(self):
        """
        Test a valid POST request to the reservation update view.
        
        This test submits a valid update to an existing reservation and checks that 
        the user is redirected to the confirmation page and the reservation is updated in the database.
        """
        timeslot = TimeSlot.objects.create(time="12:00:00")
        reservation = Reservation.objects.create(
            user_id=self.user,
            date='2024-09-01', time=timeslot, number_of_guests=2, reservation_status=0)
        form_data = {
            'date': '2024-09-02',
            'time': timeslot.id,
            'number_of_guests': 3
        }
        response = self.client.post(reverse('update_reservation', args=[reservation.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)  
        reservation.refresh_from_db()
        self.assertEqual(reservation.number_of_guests, 3)

    def test_post_update_reservation_invalid(self):
        """
        Test an invalid POST request to the reservation update view.
        
        This test submits an invalid update to an existing reservation and checks 
        that the form reloads with errors and does not update the reservation.
        """
        timeslot = TimeSlot.objects.create(time="12:00:00")
        reservation = Reservation.objects.create(
            user_id=self.user,
            date='2024-09-01', time=timeslot, number_of_guests=2, reservation_status=0)
        form_data = {'date': '', 'time': '', 'number_of_guests': ''}  
        response = self.client.post(reverse('update_reservation', args=[reservation.pk]), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'date', 'This field is required.')
        self.assertFormError(response, 'form', 'time', 'This field is required.')

    def test_get_reservation_confirmed(self):
        """
        Test the GET request to the reservation confirmation view.
        
        This test checks that the reservation confirmation page is rendered correctly 
        with a status code of 200, the correct template is used, and the reservation 
        details are displayed.
        """
        timeslot = TimeSlot.objects.create(time="12:00:00")
        reservation = Reservation.objects.create(
            date='2024-09-01', time=timeslot, number_of_guests=2, reservation_status=0)
        response = self.client.get(reverse('reservation_confirmed', args=[reservation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_confirmed.html')
        self.assertContains(response, reservation.date)

    def test_get_reservation_list_authenticated(self):
        """
        Test the GET request to the reservation list view for an authenticated user.
        
        This test checks that the reservation list is rendered correctly with a 
        status code of 200 and the correct template is used.
        """
        response = self.client.get(reverse('reservation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_list.html')

    def test_get_reservation_list_unauthenticated(self):
        """
        Test the GET request to the reservation list view for an unauthenticated user.
        
        This test checks that an unauthenticated user is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse('reservation_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/templates/account/login.html')