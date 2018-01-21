from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from core.models import Song, Album, Game
from core.calculator import calculate
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from collections import OrderedDict
import random, requests, shutil
from core.download_songs import load

# Shows two unique, randomly selected songs with screenshot, title, and description
def home(request):
    #load()
    #update_images()
    #User made a selection
    if request.method == 'POST': #TODO not very DRY. refactor to get rid of repetitive code
        if "song-1-selected" in request.POST:
            song1 = Song.objects.filter(title=request.POST['first_song_title'])[0]
            song2 = Song.objects.filter(title=request.POST['second_song_title'])[0]
            new_rating1, new_rating2 = calculate(song1.rating, song2.rating, 1)
            game = Game.objects.create(player1=song1, player2=song2, result=1, player1_pre=song1.rating,
                                       player1_post=new_rating1, player2_pre=song2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - song1.rating, player2_delta = new_rating2 -
                                       song2.rating)
            song1.rating, song2.rating = new_rating1, new_rating2
            song1.save()
            song2.save()
            return HttpResponseRedirect('/')

        elif "song-2-selected" in request.POST:
            song1 = Song.objects.filter(title=request.POST['first_song_title'])[0]
            song2 = Song.objects.filter(title=request.POST['second_song_title'])[0]
            new_rating1, new_rating2 = calculate(song1.rating, song2.rating, 0)
            Game.objects.create(player1=song1, player2=song2, result=0, player1_pre=song1.rating,
                                       player1_post=new_rating1, player2_pre=song2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - song1.rating, player2_delta = new_rating2 -
                                       song2.rating)
            song1.rating, song2.rating = new_rating1, new_rating2
            song1.save()
            song2.save()
            return HttpResponseRedirect('/')
        elif "draw" in request.POST:
            song1 = Song.objects.filter(title=request.POST['first_song_title'])[0]
            song2 = Song.objects.filter(title=request.POST['second_song_title'])[0]
            new_rating1, new_rating2 = calculate(song1.rating, song2.rating, 0.5)
            game = Game.objects.create(player1=song1, player2=song2, result=0.5, player1_pre=song1.rating,
                                       player1_post=new_rating1, player2_pre=song2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - song1.rating, player2_delta = new_rating2 -
                                       song2.rating)
            song1.rating, song2.rating = new_rating1, new_rating2
            song1.save()
            song2.save()
            return HttpResponseRedirect('/')

    #skipped, redirected, or coming to home page
    songid_1, songid_2 = get_songs()
    first_song = Song.objects.all()[songid_1] #is filtering more efficient?
    second_song = Song.objects.all()[songid_2]
    context = {'first_song': first_song, 'second_song':second_song, 'artist': first_song.artist}

    return render(request, 'home.html', context)

def rankings(request):
    songs = Song.objects.all().order_by('-rating')
    context = {'songs_list': songs, 'artist':songs[0].artist}
    return render(request, 'rankings.html', context)

# URL with no slug, redirect to url with slug
def song_detail_no_slug(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    return HttpResponseRedirect('/song/' + str(song.id) + '/' + song.slug)


# Displays the requested listing along with info about listing item, or 404 page
def song_detail(request, song_id, song_slug):
    song = get_object_or_404(Song, pk=song_id)
    if song_slug != song.slug: #Ensures song always appears with correct slug
        return HttpResponseRedirect('/song/' + str(song.id) + '/' + song.slug)
    try:
        games = Game.objects.filter(Q(player1=song)| Q(player2=song)).order_by('-id')[:10]
        try:
            if games[9].player1.id == song.id:
                rating_change = song.rating - games[9].player1_pre
            else:
                rating_change = song.rating - games[9].player2_pre
        except IndexError: #Episode has been rated fewer than 10 times
            rating_change = None
    except ObjectDoesNotExist:
        games = None
    context = {'song': song, 'games':games, 'rating_change':rating_change, 'artist':song.artist}
    return render(request, 'song_detail.html', context)

#Displays list of songs in album in descending rating order,
def album_detail(request, album_id):
    songs = Song.objects.filter(album=album_id).order_by('id')
    album = get_object_or_404(Album, id=album_id)
    if not songs: #Non-existent album, return to album rankings page
        raise Http404()
    sum = 0
    min_rating = songs[0].rating
    max_rating = songs[0].rating
    min_index = 0
    max_index = 0
    for index, song in enumerate(songs):
        if song.rating < min_rating:
            min_rating = song.rating
            min_index = index
        elif song.rating > max_rating:
            max_rating = song.rating
            max_index = index
        sum += song.rating
    average = round(sum/songs.count(), 1)

    context = {'songs':songs, 'average_rating':average, 'album': album, 'best_song':songs[max_index],
               'worst_song':songs[min_index], 'artist':songs[0].artist}
    return render(request, 'album_detail.html', context )

def album_rankings(request): #TODO REFACTOR
    num_songs = {}
    album_sums = {}
    ratings = {}
    rankings = OrderedDict()
    for song in Song.objects.all():
        if song.album in num_songs and song.album in album_sums:
            num_songs[song.album]+= 1
            album_sums[song.album] += song.rating
        else:
            num_songs[song.album] = 1
            album_sums[song.album] = song.rating

    for album in album_sums:
        ratings[album] = round(album_sums[album]/num_songs[album],1)#average rating for each album

    sorted_albums = sorted(ratings, key=ratings.__getitem__, reverse=True)

    for album in sorted_albums:
        rankings[album] = ratings[album]

    context = {'rankings':rankings, 'artist': Song.objects.all()[0].artist }
    return render(request, 'album_rankings.html', context)

def about(request):
    artist = Song.objects.all()[0].artist
    vote_count = Game.objects.all().count()
    context = {'artist':artist,'vote_count': vote_count}
    return render(request, 'about.html', context)

#Helper method to generate random song IDs
def get_songs():
    total_songs = Song.objects.count()
    song_1 = random.randint(0, total_songs - 1)
    song_2 = random.randint(0, total_songs - 1)
    while song_1 == song_2: #ensures random
        song_2 = random.randint(0, total_songs - 1)

    return song_1, song_2

#Helper method for updating slugs--only needed for updating existing database as new databases will have slugs upon creation
def update_slugs():
    for song in Song.objects.all():
        song.save()

#Helper method for adding game deltas--only need for updating existing database
def update_games():
    for game in Game.objects.all():
        game.player1_delta = game.player1_post - game.player1_pre
        game.player2_delta = game.player2_post - game.player2_pre
        game.save()

#Helper method for downloading images
def update_images():
    for song in Song.objects.all():
        if '.jpg' in song.image_src or '.jpeg' in song.image_src:
            extension = '.jpg'
        else:
            extension = '.png'
        response = requests.get(song.image_src, stream=True)
        with open('static/images/song/{0}{1}'.format(song.title.replace('?',''), extension), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            out_file.close()
        song.image = '../images/song/{0}{1}'.format(song.title.replace('?', ''), extension)
        song.save()

    for album in Album.objects.all():
        if '.jpg' in album.image_src or '.jpeg' in album.image_src:
            extension = '.jpg'
        else:
            extension = '.png'
        response = requests.get(album.image_src, stream=True)
        with open('static/images/album/{0}{1}'.format(album.title.replace('?', ''), extension), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            out_file.close()
        album.image = '../images/album/{0}{1}'.format(album.title.replace('?', ''), extension)
        album.save()
