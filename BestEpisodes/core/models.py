from django.db import models


class Episode(models.Model):
    imdb_id = models.TextField()
    series = models.TextField()
    season = models.IntegerField(default=0)
    episode = models.IntegerField(default=0)
    title = models.TextField()
    plot = models.TextField()
    image_src = models.URLField()
    image = models.ImageField()
    rating = models.DecimalField(decimal_places=1, max_digits=5, default=1000)

    def __str__(self):
        return "Season "+ str(self.season) + " episode " + str(self.episode) + ": " + self.title

class Game(models.Model):
    player1 = models.ForeignKey(Episode, related_name='Games_Player1')
    player2 = models.ForeignKey(Episode, related_name='Games_Player2')
    result = models.DecimalField(decimal_places=1, max_digits=2)
    player1_pre = models.DecimalField(decimal_places=1, max_digits=5)
    player1_post = models.DecimalField(decimal_places=1, max_digits=5)
    player2_pre = models.DecimalField(decimal_places=1, max_digits=5)
    player2_post = models.DecimalField(decimal_places=1, max_digits=5)

    def __str__(self):
        return "Game " + str(self.id) + " "+ self.player1.title + " vs " + self.player2.title