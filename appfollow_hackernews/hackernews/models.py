from django.db import models


class Post(models.Model):
    def __str__(self):  # pragma: no cover
        return f'“{self.title}“ {self.url}'

    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    created = models.DateTimeField('date created', auto_now_add=True)
