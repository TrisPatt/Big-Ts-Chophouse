from django.contrib import admin
from .models import Review

@admin.register(review)
class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('user', 'overall_rating', 'comment', 'creaed_on')
