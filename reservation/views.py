from django.shortcuts import render, redirect
from django.views import generic
from .models import reservation
from .forms import reservationForm


# Create your views here.
def reservation_list(request):
    reservations = reservation.objects.all()
    return render(request, '/workspace/Big-Ts-Chophouse/reservation/templates/reservation/reservation_list.html', {'reservations': reservations})

def reservation_create(request):
    if request.method == 'POST':
        form = reservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = reservationForm()
    return render(request, '/workspace/Big-Ts-Chophouse/reservation/templates/reservation/reservation_form.html', {'form': form})