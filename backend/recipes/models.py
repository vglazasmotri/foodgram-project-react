from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200)
    cooking_time = models.PositiveIntegerField()
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
