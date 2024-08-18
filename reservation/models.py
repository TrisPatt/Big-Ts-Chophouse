from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.conf import settings
from cloudinary.models import CloudinaryField
from datetime import date


STATUS = ((0, "confirmed"), (1, "cancelled"), (2, "expired"))

class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)  # Unique table identifier
    seats = models.PositiveIntegerField(default=2)  # All tables have 2 seats by default

    def __str__(self):
        return f"Table {self.table_number} - {self.seats} seats"

class TimeSlot(models.Model):
    time = models.TimeField()
    
    def __str__(self):
        return self.time.strftime('%H:%M')


class Reservation(models.Model):
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
        return f"{self.date} - {self.time}"


    def save(self, *args, **kwargs):
        # If the reservation date has past, set status to expired
        if self.date < date.today():
            self.reservation_status = 2

        # Creates a unique reservation number automaticaaly for each booking new booking
        if not self.pk:  
            last_reservation = Reservation.objects.aggregate(Max('reservation_number'))
            max_number = last_reservation['reservation_number__max'] or 0
            self.reservation_number = max_number + 1

        # Automatically set the status to confirmed (0)
            if self.reservation_status is None:
                self.reservation_status = 0

        # Ensure cancelled reservations cant be modified
        if self.pk:  
            existing_reservation = Reservation.objects.get(pk=self.pk)
            if existing_reservation.reservation_status == 1 and self.reservation_status != 1:
                raise ValidationError("You cannot modify a canceled reservation.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.user_id} on {self.date} at {self.time}"

