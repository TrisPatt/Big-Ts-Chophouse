from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date


STATUS = ((0, "confirmed"), (1, "cancelled"), (2, "expired"))


class Table(models.Model):
    """
    Model to handle the tables and seats per table.

    The default seats per table is currently set to 2.
    """
    table_number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(default=2)

    def __str__(self):
        return f"Table {self.table_number} - {self.seats} seats"


class TimeSlot(models.Model):
    """
    Model to handle the available time slots per date.

    These can be adjusted if necessary in the admin panel.
    """
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime('%H:%M')


class Reservation(models.Model):
    """
    Model representing a reservation in the restaurant.

    The reservation number is a unique identifier for the reservation and is
    automatically assigned through custom logic.
    The user ID is a foreign key linking to the user model, representing the
    user who made the reservation.
    The time is a foreign key linking to the TimeSlot model, representing the
    time of the reservation.
    The reservation status is represented as an integer as stated above for
    either confirmed (0),
    cancelled(1) or expired(2).
    Created on is an automatic timestamp when the reservation was made.
    Tables is a many to many relationship with the Table model, representing
    the tables reserved.

    - Automatically generates a unique reservation number for new reservations.
    - Sets the reservation status to 'expired' if the reservation date is in
    the past.
        (This is to validate dates from the past, which should not be possible
        from the front end and is additional validation)
    - Ensures that the status is automatically set to 'confirmed' if not
    already set.
    - Prevents modifications to reservations that have been cancelled.
        (This should not be possible from the front end and is additional
        validation)
    - Ensure that cancelled reservations cannot be modified.

    """
    reservation_number = models.IntegerField(unique=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    date = models.DateField()
    time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    number_of_guests = models.IntegerField()
    allergies = models.TextField(blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    reservation_status = models.IntegerField(choices=STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    tables = models.ManyToManyField(Table, related_name='reservations')

    def __str__(self):
        return f'Reservation at {self.time.time.strftime('%H:%M')}' 

    def save(self, *args, **kwargs):
        if not self.pk:
            last_reservation = Reservation.objects.aggregate(
                Max('reservation_number')
            )
            max_number = last_reservation['reservation_number__max'] or 0
            self.reservation_number = max_number + 1

        if self.date < date.today():
            if self.pk:
                self.reservation_status = 2
            else:
                raise ValidationError("""Cannot create a reservation for a past
                                        date.""")

        if self.reservation_status is None:
            self.reservation_status = 0

        if self.pk:
            existing_reservation = Reservation.objects.get(pk=self.pk)
            if (existing_reservation.reservation_status == 1 and
                    self.reservation_status != 1):
                raise ValidationError(
                    "You cannot modify a cancelled reservation."
                    )

        super().save(*args, **kwargs)
