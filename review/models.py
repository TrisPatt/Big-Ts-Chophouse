from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField()
    overall_rating = models.PositiveIntegerField()
    food_rating = models.PositiveIntegerField()
    service_rating = models.PositiveIntegerField()
    ambience_rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} - Rating: {self.overall_rating}'
