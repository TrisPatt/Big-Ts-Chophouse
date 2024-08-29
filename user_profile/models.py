from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    A model that extends the default Django User model by adding additional
    fields such as phone number and date of birth.
    The string method returns the user associated with the profile.

    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    A signal receiver that creates or updates a Profile instance
    whenever a User instance is created or updated.

    This ensures that every User has a corresponding Profile.

    Args:
        sender (Model): The model class that sent the signal (in this case,
        User).
        instance (User): The actual instance of the model that's being saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments passed by the signal.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
