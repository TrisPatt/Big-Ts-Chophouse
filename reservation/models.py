from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

STATUS = ((0, "confirmed"), (1, "cancelled"))

# Create your models here.
class Reservation(models.Model):
    reservation_number = models.IntegerField(unique=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    allergies = models.TextField(blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    reservation_status = models.IntegerField(choices=STATUS)
    created_on = models.DateTimeField(auto_now_add=True)


    # Creates a unique reservation number automaticaaly for each booking to save multiple reservation numbers being created
    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created
            last_reservation = Reservation.objects.aggregate(Max('reservation_number'))
            max_number = last_reservation['reservation_number__max'] or 0
            self.reservation_number = max_number + 1

        # Automatically set the status to confirmed (0)
            if self.reservation_status is None:
                self.reservation_status = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.user_id} on {self.date} at {self.time}"

