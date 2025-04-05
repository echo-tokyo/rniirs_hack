from django.db import models

from users.models import CustomUser


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)


class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


# class Favorite(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
