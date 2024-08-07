from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "confirmed"), (1, "cancelled"))

# Create your models here.
class reservation(models.Model):
    reservation_number = models.IntegerField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
    allergies = models.TextField()
    special_requirements = models.TextField()
    reservation_status = models.IntegerField(choices= STATUS)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.user_id} on {self.date} at {self.time}"

