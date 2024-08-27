from django_cron import CronJobBase, Schedule
from datetime import date
from reservation.models import Reservation


class ExpiredReservationsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 1440 minutes = 24 hours (runs once daily)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reservation.expired_reservations_cron_job'  # a unique code

    def do(self):
        # Update all reservations with a past date to 'expired'
        expired_reservations = Reservation.objects.filter(date__lt=date.today(), reservation_status=0)

        updated_count = expired_reservations.update(reservation_status=2)
        print(f'{updated_count} reservations have been updated to expired.')
