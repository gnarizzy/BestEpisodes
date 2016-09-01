from django.db import models


class Episode(models.Model):
    imdb_id = models.TextField()
    series = models.TextField()
    season = models.IntegerField(default=0)
    episode = models.IntegerField(default=0)
    title = models.TextField()
    plot = models.TextField()
    image = models.URLField()
    rating = models.DecimalField(decimal_places=1, max_digits=5, default=1000)

    def __str__(self):
        return "Season "+ str(self.season) + " episode " + str(self.episode) + ": " + self.title

