from django import forms
from .models import Review
from django.utils import timezone
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    """
    A form for submitting reviews.

    This form is used to collect and validate review information from users.
    It includes fields for various aspects of the review, such as ratings and
    comments, and includes validation to ensure that the visit date is not set
    in the future.

    Uses a DateInput widget with the 'form-control datepicker' class and an ID
    of 'visit-date' for date selection.

    """
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
        """
        Validates that the visit date is not in the future.

        This method is called during form validation to ensure that the visit
        date entered by the user is not a future date. If the date is in the
        future, a ValidationError is raised.

        """

        if visit_date and visit_date > timezone.now().date():
            raise ValidationError("The visit date cannot be in the future.")

        return visit_date
