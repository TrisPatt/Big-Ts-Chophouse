from django.contrib import admin
from .models import Reservation, Table, TimeSlot
from django_summernote.admin import SummernoteModelAdmin

"""
This module registers the Table, Reservation, and TimeSlot models with the
Django admin interface and customizes their appearance and functionality.
"""


@admin.register(Table)
class TableAdmin(SummernoteModelAdmin):
    """
    The TableAdmin class customizes the admin view for the Table model,
    displaying the table number and the number of seats in the list view.
    """
    list_display = ('table_number', 'seats')


@admin.register(Reservation)
class ReservationAdmin(SummernoteModelAdmin):
    """
    The ReservationAdmin class customizes the admin view for the Reservation
    model:
    - Displays fields such as user ID, reservation number, date, time, related
    tables, and reservation status in the list view.
    - Allows searching by the 'allergies' field.
    - Adds filters for 'reservation_status' and 'date'.
    - Integrates the Summernote rich text editor for the 'allergies' and
    'special_reqs' fields.
    - Defines a custom method to display the related tables for a reservation
    as a comma-separated
        list in the list view.
    """

    list_display = ('user_id', 'reservation_number', 'date', 'time',
                    'get_tables', 'reservation_status')
    search_fields = ['allergies']
    list_filter = ('reservation_status', 'date')
    summernote_fields = ('allergies', 'special_reqs')

    def get_tables(self, obj):
        return ", ".join([str(table) for table in obj.tables.all()])
    get_tables.short_description = 'Tables'


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """
    The TimeSlotAdmin class customizes the admin view for the TimeSlot model,
    displaying the time field and adding a filter option for it in the list
    view.
    """
    list_display = ['time']
    list_filter = ['time']








