from django.urls import path
from . import views

urlpatterns = [
    path('submit_review/', views.submit_review, name='submit_review'),
    path('reviews/', views.review_list, name='review_list'),
]