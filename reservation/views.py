from django.shortcuts import render, redirect
from .models import Reservation
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from .forms import CancelReservationForm


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

@login_required #cancel reservations once logged in
def cancel_reservation(request, reservation_number):
    reservation = get_object_or_404(Reservation, reservation_number=Reservation_number)
    
    if request.method == 'POST':
        form = CancelReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')  # Redirect to a list of reservations 
    else:
        form = CancelReservationForm(instance=reservation)
    
    return render(request, 'reservation/cancel_reservation.html', {'form': form, 'reservation': reservation})