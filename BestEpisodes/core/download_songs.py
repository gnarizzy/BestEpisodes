#A script to load all song data into the database
import requests, shutil, json
from core.models import Song, Album
import pprint



ARTIST = "Taylor Swift"

def load():
    with open('core/songs.json') as json_data:
        data = json.load(json_data)

    for song in data:
        try:
            album = Album.objects.get(title=song['Album'])
        except:
            album = None
        if not album:
            album = Album.objects.create(title=song['Album'], image_src=song['Image'], artist=ARTIST)
        Song.objects.create(album=album, title=song['Song'], year=song['Year'], image_src=song['Image'], artist=ARTIST)