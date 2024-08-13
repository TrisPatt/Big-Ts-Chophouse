from . import views
from django.urls import path

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('', views.reservation_confirmed, name='reservation_confirmed'),
    path('create/', views.reservation_create, name='reservation_create'),
    path('reservation/confirmed/', views.reservation_confirmed, name='reservation_confirmed'),
    path('reservation/<int:reservation_number>/cancel/', views.cancel_reservation, name='cancel_reservation'),
]


