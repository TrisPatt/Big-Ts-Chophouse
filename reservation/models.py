from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "confirmed"), (1, "cancelled"))

# Create your models here.
class reservation(models.Model):
    reservation_num = models.IntegerField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    num_of_guests = models.IntegerField()
    allergies = models.TextField()
    special_reqs = models.TextField()
    reservation_status = models.IntegerField(choices= STATUS)
    created_on = models.DateTimeField(auto_now_add=True)

