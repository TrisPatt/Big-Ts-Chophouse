"""
URL configuration for Big project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reservation import views as reservation_views
from review import views as review_views
from menu import views as menu_views


urlpatterns = [
    path('', reservation_views.home, name='home'),
    path('reservation/', include('reservation.urls'), name='reservation-urls'),
    path('review/', review_views.my_review, name='review'),
    path('summernote/', include('django_summernote.urls')),
    path("accounts/", include("allauth.urls")),
    path('menu/', include('menu.urls')),
    path('admin/', admin.site.urls),
]
