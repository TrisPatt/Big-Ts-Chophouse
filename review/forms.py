from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['visit_date', 'overall_rating', 'food_rating', 'service_rating', 'ambience_rating', 'comment']

