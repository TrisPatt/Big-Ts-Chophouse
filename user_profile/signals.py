from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that ensures a Profile is created for each User instance.

    This function is triggered whenever a User instance is saved. If the User
    is newly created, it attempts to create a corresponding Profile. If the
    User already existed but didn't have an associated Profile, it will create
    one to ensure consistency.

    """
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
