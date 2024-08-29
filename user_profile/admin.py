from django.contrib import admin
from .models import Profile


admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    """
    The ProfileAdmin class customizes the admin view for the Profile model,
    displaying the additional user details in the list view.
    """
    list_display = ('user', 'first_name', 'last_name', 'email_address',
                    'phone_number')
