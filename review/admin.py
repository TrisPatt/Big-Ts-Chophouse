from django.contrib import admin
from .models import Review
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the Review model.

    This class customizes the Django admin interface for the Review model
    by using the Summernote WYSIWYG editor for rich text fields.
    
    """

    list_display = ('user', 'overall_rating', 'comment', 'created_on')
