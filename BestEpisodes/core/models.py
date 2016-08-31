from django.db import models

class Episode(models.Model):
    IMDB_ID = models.TextField(default="")
    series = models.TextField(default="")
    season = models.IntegerField(default=0)
    title = models.TextField(default="")
    plot = models.TextField(default="")
    image = models.URLField(default="")
    rating = models.DecimalField(decimal_places=1, max_digits=5, default=1000)

