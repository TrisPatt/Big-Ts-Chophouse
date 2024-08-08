from django.contrib import admin
from .models import Reservation
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Reservation)


class ReservationAdmin(SummernoteModelAdmin):

    list_display = ('date', 'time', 'reservation_status')
    search_fields = ['allergies']
    list_filter = ('reservation_status',)
    summernote_fields = ('allergies', 'special_reqs')

# Register your models here.


