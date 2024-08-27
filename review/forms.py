from django import forms
from .models import Review
from django.utils import timezone
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'visit_date', 'overall_rating', 'food_rating',
                  'service_rating', 'ambience_rating', 'comment']
        widgets = {
            'visit_date': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'id': 'visit-date',

            })
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')

        # Ensure the visit date is not in the future
        if visit_date and visit_date > timezone.now().date():
            raise ValidationError("The visit date cannot be in the future.")

        return visit_date
