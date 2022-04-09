from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    content = models.TextField()
    tag = models.CharField(max_length=30)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    rate_one = models.PositiveSmallIntegerField(default=0)
    rate_two = models.PositiveSmallIntegerField(default=0)
    rate_three = models.PositiveSmallIntegerField(default=0)
    rate_four = models.PositiveSmallIntegerField(default=0)
    rate_five = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

class Rate(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_rated = models.PositiveSmallIntegerField(
        default = 0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    comment = models.CharField(max_length=280)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.is_rated)