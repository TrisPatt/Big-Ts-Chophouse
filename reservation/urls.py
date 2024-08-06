from . import views
from django.urls import path

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('new/', views.reservation_create, name='reservation_create'),
]


