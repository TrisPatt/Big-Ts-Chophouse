from django.urls import path
from . import views

urlpatterns = [
    path('submit_review/', views.submit_review, name='submit_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]