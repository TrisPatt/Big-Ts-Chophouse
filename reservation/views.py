from django.shortcuts import render, redirect
from .models import reservation
from .forms import reservationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'reservation/home.html')

def reservation_list(request):
    reservations = reservation.objects.all()
    return render(request, 'reservation/reservation_list.html', {'reservations': reservations})


@login_required #Only allow logged in users to create a reservation with their unique id
def reservation_create(request):
    if request.method == 'POST':
        form = reservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user_id = request.user
            reservation.save()
            return redirect('reservation_list')
    else:
        form = reservationForm()
    return render(request, 'reservation/reservation_form.html', {'form': form})