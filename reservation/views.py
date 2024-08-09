from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm, CancelReservationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# home page
def home(request):
    return render(request, 'reservation/home.html')

#review reservations
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation/reservation_list.html', {'reservations': reservations})


@login_required #Only allow logged in users to create a reservation with their unique id
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'reservation/reservation_form.html', {'form': form})

@login_required # Cancel reservations once logged in
def cancel_reservation(request, reservation_number):
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number)

    if reservation.reservation_status == 1:
        messages.info(request, 'This reservation has been cancelled.')
        return redirect('reservation_list')
    
    if request.method == 'POST':
        form = CancelReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation.reservation_status = 1
            form.save() # Save the reservation with the new status
            messages.success(request, 'Your reservation has been successfully cancelled.') # Display confirmation message

            send_mail(
                'Reservation Cancelled',
                f'Your reservation on {reservation.date} at {reservation.time} has been successfully cancelled.',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('reservation_list')  # Redirect to a list of reservations 
    else:
        form = CancelReservationForm(instance=reservation)
    
    return render(request, 'reservation/cancel_reservation.html', {'form': form, 'reservation': reservation})