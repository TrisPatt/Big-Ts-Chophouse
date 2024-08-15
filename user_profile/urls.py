from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('user_profile/', views.profile_update, name='profile'), 
    path('update/confirmed/', views.profile_update_confirmation, name='profile_confirmed'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]