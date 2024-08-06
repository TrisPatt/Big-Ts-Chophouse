from . import views
from django.urls import path

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('create/', views.reservation_create, name='reservation_create'),
]


