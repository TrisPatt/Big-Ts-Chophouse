from django.shortcuts import render, redirect
from django.views import generic

# Create your views here.
def home(request):
    return render(request, '/workspace/Big-Ts-Chophouse/Big/index.html')