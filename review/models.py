from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateField()
    title = models.CharField(max_length=50)
    overall_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    food_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    service_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    ambience_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} - Rating: {self.overall_rating}'
