from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    """
    A model representing a user review for the restaurant.

    This model stores reviews submitted by users, including their ratings,
    along with a comment and other relevant details.

    The user is a foreign key to the built in user model. It is set to cascade
    meaning if the user is deleted, their reviews are also deleted.

    The rating fields are integers set in range from 1 to 5. This is rendered
    on the review as stars.

    The __str__ method returns a string representation of the review, including
    the username of the reviewer and their overall rating.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField()
    title = models.CharField(max_length=50)
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    food_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    service_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    ambience_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""Review by {self.user.username} -
        Rating: {self.overall_rating}"""
