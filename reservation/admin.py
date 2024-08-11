from django.contrib import admin
from .models import Reservation, Table
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Table)
class TableAdmin(SummernoteModelAdmin):
    list_display = ('table_number', 'seats')


@admin.register(Reservation)
class ReservationAdmin(SummernoteModelAdmin):

    list_display = ('user_id', 'reservation_number', 'date', 'time','get_tables', 'reservation_status')
    search_fields = ['allergies']
    list_filter = ('reservation_status', 'date')
    summernote_fields = ('allergies', 'special_reqs')

    def get_tables(self, obj):
        return ", ".join([str(table) for table in obj.tables.all()])
    get_tables.short_description = 'Tables'







