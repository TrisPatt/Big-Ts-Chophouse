from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('user_profile/', views.profile_update, name='profile'),
    path('update/profile/', views.profile_update, name='profile_update'),
    path('update/confirmed/', views.profile_update_confirmation,
         name='profile_confirmed'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('my_account/', views.my_account, name='my_account'),
]
