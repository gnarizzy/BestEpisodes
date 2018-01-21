from django.db import models
from django.utils.text import slugify


class Album(models.Model):
    title = models.CharField(max_length=160)
    artist = models.CharField(max_length=160)
    image_src = models.URLField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    artist = models.CharField(max_length=160)
    image_src = models.URLField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    rating = models.DecimalField(decimal_places=1, max_digits=5, default=1000)
    year = models.IntegerField()
    slug = models.SlugField()
    stream_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Song, self).save(*args, **kwargs)

class Game(models.Model):
    player1 = models.ForeignKey(Song, related_name='Games_Player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Song, related_name='Games_Player2', on_delete=models.CASCADE)
    result = models.DecimalField(decimal_places=1, max_digits=2)
    player1_pre = models.DecimalField(decimal_places=1, max_digits=5)
    player1_post = models.DecimalField(decimal_places=1, max_digits=5)
    player2_pre = models.DecimalField(decimal_places=1, max_digits=5)
    player2_post = models.DecimalField(decimal_places=1, max_digits=5)
    player1_delta = models.DecimalField(decimal_places=1, max_digits=5)
    player2_delta = models.DecimalField(decimal_places=1, max_digits=5)

    def __str__(self):
        return "Game {0}: {1} vs {2}".format(str(self.id), self.player1.title, self.player2.title)


