from . import views
from django.urls import path

urlpatterns = [
    
    path('user_profile/', views.profile_update, name='profile'), 
    path('update/confirmed/', views.profile_update_confirmation, name='profile_confirmed'), 
]