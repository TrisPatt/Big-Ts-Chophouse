from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Signal to create or update user profile when user object is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()