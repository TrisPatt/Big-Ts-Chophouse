from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Reservation, Table, TimeSlot
from .forms import ReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from datetime import date


def home(request):
    """
    Render the home page
    """
    return render(request, 'reservation/home.html')


# Confirmed reservation
def reservation_confirmed(request, reservation_number):
    """
    Render the reservation confirmation page.

    Fetches and displays the reservation details based on the provided
    reservation number.

    Args:
        reservation_number: The unique identifier for the reservation.

    Returns:
        A rendered HTML page with reservation details.
    """
    reservation = get_object_or_404(Reservation, pk=reservation_number)
    return render(request, 'reservation/reservation_confirmed.html',
                  {'reservation': reservation})


@login_required
def reservation_list(request):
    """
    Display a list of reservations for the logged-in user.

    Fetches and displays reservations made by the logged-in user,
    sorted by date in descending order.

    Returns a rendered HTML page with a list of reservations.
    """
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user_id=request.user.id).order_by('-date')
        return render(request, 'reservation/reservation_list.html',
                      {'reservations': reservations})
    else:
        return redirect('templates/account/login.html')


@login_required
def reservation_create(request):
    """
    Handle the creation of a new reservation.

    Handles the reservation creation form, checks table availability,
    and sends a confirmation email to the user. If the reservation cannot
    be accommodated, an error message is shown.

    Returns a rendered HTML page with the reservation creation form or a redirect
    to the confirmation page upon successful creation.
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            reservation.save()

            num_guests = reservation.number_of_guests
            tables_needed = (num_guests + 1) // 2

            available_tables = Table.objects.annotate(
                reserved_count=models.Count('reservations', filter=models.Q(
                    reservations__date=reservation.date,
                    reservations__time=reservation.time,
                    reservations__reservation_status=0
                ))
            ).filter(reserved_count=0).count()

            if tables_needed <= available_tables:
                tables = Table.objects.annotate(
                    reserved_count=models.Count
                    ('reservations', filter=models.Q(
                        reservations__date=reservation.date,
                        reservations__time=reservation.time,
                        reservations__reservation_status=0
                    ))
                ).filter(reserved_count=0)[:tables_needed]

                reservation.tables.add(*tables)
                reservation.save()

                send_mail(
                'Reservation Confirmed!',
                f"""Your reservation on {reservation.date} at {reservation.time} 
                has been successfully booked.""",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
                )

                return redirect('reservation_confirmed',
                                reservation_number=reservation.pk)

            else:
                messages.error(request, """Sorry, we can't accommodate your party
                               size at the requested time.""")
                return redirect('reservation_create')
    else:
        form = ReservationForm(user=request.user)

    return render(request, 'reservation/reservation_form.html', {'form': form})


def available_time_slots(request):
    """
    Display available time slots based on the selected date.

    Retrieves the available time slots for reservations on the selected
    date, excluding fully booked slots.

    Returns a rendered HTML page with available time slots.
    """
    selected_date = request.GET.get('date', date.today())
    all_time_slots = TimeSlot.objects.all()

    booked_slots = (
    Reservation.objects
    .filter(date=selected_date, reservation_status=0)
    .values('time')
    .annotate(total_guests=Sum('number_of_guests'))
    .filter(total_guests__gte=24)
)
    available_slots = all_time_slots.exclude(id__in=[slot['time']
                                                     for slot in booked_slots])

    return render(request, 'available_time_slots.html',
                  {'available_slots': available_slots})


@login_required
def cancel_reservation(request, reservation_number):
    """
    Handle the cancellation of an existing reservation.

    Fetches the reservation based on the reservation number, updates its
    status to 'cancelled', and sends a cancellation confirmation email to
    the user. Redirects to the reservation list page upon success.

    Args:
        reservation_number: The unique identifier for the reservation.

    Returns a rendered HTML page to confirm cancellation and a redirect to
    the reservation list page upon successful cancellation or cancelled cancellation.
    """
    reservation = get_object_or_404(
        Reservation, reservation_number=reservation_number, user_id=request.user
    )

    if request.method == 'POST':       
        reservation.reservation_status = 1  
        reservation.save()
        send_mail(
            'Reservation Cancelled',
            f"""Your reservation on {reservation.date} at {reservation.time}
            has been successfully cancelled.""",
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

        messages.success(
            request, 'Your reservation has been successfully cancelled.'
        )
        return redirect('reservation_list')

    return render(request, 'reservation/cancel_reservation.html',
                    {'reservation': reservation})


@login_required
def update_reservation(request, reservation_number):
    """
    Handle the update of an existing reservation.

    Fetches the reservation based on the reservation number, validates
    the updated reservation details, checks table availability, and
    sends a confirmation email for the updated reservation. Redirects to
    the confirmation page upon successful update.

    Args:
        reservation_number: The unique identifier for the reservation.

    Returns a rendered HTML page with the reservation update form or a redirect
    to the confirmation page upon successful update.
    """
    try:
        reservation = Reservation.objects.get(reservation_number=reservation_number)
        print(f"Logged-in user: {request.user}")
        print(f"Reservation user: {reservation.user_id}")
    except Reservation.DoesNotExist:
        print("Reservation does not exist")
        raise

    if reservation.user_id != request.user:
        print("Reservation does not belong to the logged-in user.")
        return redirect('reservation_list')

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            updated_reservation.user_id = request.user

            num_guests = updated_reservation.number_of_guests
            tables_needed = (num_guests + 1) // 2  

            total_guests_at_time = Reservation.objects.filter(
            date=updated_reservation.date,
            time=updated_reservation.time,
            reservation_status=0
            ).exclude(pk=updated_reservation.pk).aggregate(
            total_guests=models.Sum('number_of_guests')
            )['total_guests'] or 0

            if total_guests_at_time + num_guests > 24:
                messages.error(request, """Sorry, we cannot accommodate your
                               party size at the requested time.""")
                return render(request, 'reservation/reservation_form.html',
                              {'form': form, 'reservation': reservation})

            available_tables = Table.objects.annotate(
                reserved_count=models.Count('reservations', filter=models.Q(
                    reservations__date=updated_reservation.date,
                    reservations__time=updated_reservation.time,
                    reservations__reservation_status=0
                ))
            ).filter(reserved_count=0).count()

            if tables_needed <= available_tables:
                updated_reservation.tables.clear()

                available_tables = Table.objects.annotate(
                    reserved_count=models.Count
                    ('reservations', filter=models.Q(
                        reservations__date=updated_reservation.date,
                        reservations__time=updated_reservation.time,
                        reservations__reservation_status=0
                    ))
                ).filter(reserved_count=0)[:tables_needed]

                updated_reservation.tables.add(*available_tables)
                updated_reservation.save()

                send_mail(
                    'Reservation Updated!',
                    f"""Your reservation has been updated to
                    {updated_reservation.date} at {updated_reservation.time}.""",
                    settings.DEFAULT_FROM_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )

                messages.success(request, """Your reservation has been
                                 successfully updated.""")
                return redirect('reservation_confirmed',
                                reservation_number=updated_reservation.pk)
            else:
                messages.error(request, """Sorry, not enough tables are
                               available for your party size.""")
                return render(request, 'reservation/reservation_form.html',
                              {'form': form, 'reservation': reservation})
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservation/reservation_form.html',
                  {'form': form, 'reservation': reservation})

    