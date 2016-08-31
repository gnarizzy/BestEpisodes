from django.db import models

class Episode(models.Model):
    IMDB_ID = models.TextField(default="")
    series = models.TextField(default="")
    season = models.IntegerField(default=0)
    title = models.TextField(default="")
    plot = models.TextField(default="")
    image = models.URLField(default="")

