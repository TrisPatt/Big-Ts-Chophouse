from django_cron import CronJobBase, Schedule
from datetime import date
from reservation.models import Reservation


class ExpiredReservationsCronJob(CronJobBase):
    """
    This module defines a cron job for managing expired reservations.

    The `ExpiredReservationsCronJob` class is a scheduled task that updates the status of reservations 
    when their date has 'expired'. 

    - The cron job is configured to run every 1440 minutes (24 hours) using the `django_cron` library.
    - It filters reservations with a date earlier than today and a status of 'active' (0).
    - The status of these reservations is updated to 'expired' (2).
    - The number of updated reservations is printed to the console.
    """
    RUN_EVERY_MINS = 1440  

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reservation.expired_reservations_cron_job'  

    def do(self):
        
        expired_reservations = Reservation.objects.filter(date__lt=date.today(), reservation_status=0)

        updated_count = expired_reservations.update(reservation_status=2)
        print(f'{updated_count} reservations have been updated to expired.')
