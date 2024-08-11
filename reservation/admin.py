from django.contrib import admin
from .models import Reservation, Table
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Reservation)
@admin.register(Table)

class ReservationAdmin(SummernoteModelAdmin):

    list_display = ('user_id', 'reservation_number', 'date', 'time','tables', 'reservation_status')
    search_fields = ['allergies']
    list_filter = ('reservation_status',)
    summernote_fields = ('allergies', 'special_reqs')

# Register your models here.


