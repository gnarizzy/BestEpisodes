from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from core.models import Episode, Game
from core.calculator import calculate
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import random

# Shows two unique, randomly selected episodes with screenshot, title, and description
def home(request):
    #User made a selection
    if request.method == 'POST': #TODO not very DRY. refactor to get rid of repetitive code
        if "episode-1-selected" in request.POST:
            episode1 = Episode.objects.filter(title=request.POST['first_episode_title'])[0]
            episode2 = Episode.objects.filter(title=request.POST['second_episode_title'])[0]
            new_rating1, new_rating2 = calculate(episode1.rating, episode2.rating, 1)
            game = Game.objects.create(player1=episode1, player2=episode2, result=1, player1_pre=episode1.rating,
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - episode1.rating, player2_delta = new_rating2 -
                                       episode2.rating)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')

        elif "episode-2-selected" in request.POST:
            episode1 = Episode.objects.filter(title=request.POST['first_episode_title'])[0]
            episode2 = Episode.objects.filter(title=request.POST['second_episode_title'])[0]
            new_rating1, new_rating2 = calculate(episode1.rating, episode2.rating, 0)
            game = Game.objects.create(player1=episode1, player2=episode2, result=0, player1_pre=episode1.rating,
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - episode1.rating, player2_delta = new_rating2 -
                                       episode2.rating)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')
        elif "draw" in request.POST:
            episode1 = Episode.objects.filter(title=request.POST['first_episode_title'])[0]
            episode2 = Episode.objects.filter(title=request.POST['second_episode_title'])[0]
            new_rating1, new_rating2 = calculate(episode1.rating, episode2.rating, 0.5)
            game = Game.objects.create(player1=episode1, player2=episode2, result=0.5, player1_pre=episode1.rating,
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2,
                                       player1_delta = new_rating1 - episode1.rating, player2_delta = new_rating2 -
                                       episode2.rating)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')

    #skipped, redirected, or coming to home page
    episodeid_1, episodeid_2 = get_episodes()
    first_episode = Episode.objects.all()[episodeid_1] #is filtering more efficient?
    second_episode = Episode.objects.all()[episodeid_2]
    context = {'first_episode': first_episode, 'second_episode':second_episode}

    return render(request, 'home.html', context)

def rankings(request):
    episodes = Episode.objects.all().order_by('-rating')
    context = {'episodes_list': episodes}
    return render(request, 'rankings.html', context)

# URL with no slug, redirect to url with slug
def episode_detail_no_slug(request, episode_id):
    episode = get_object_or_404(Episode, pk=episode_id)
    return HttpResponseRedirect('/episode/' + str(episode.id) + '/' + episode.slug)


# Displays the requested listing along with info about listing item, or 404 page
def episode_detail(request, episode_id, episode_slug):
    episode = get_object_or_404(Episode, pk=episode_id)
    if episode_slug != episode.slug: #Ensures episode always appears with correct slug
        return HttpResponseRedirect('/episode/' + str(episode.id) + '/' + episode.slug)
    try:
        games = Game.objects.filter(Q(player1=episode)| Q(player2=episode)).order_by('-id')[:10]
        try:
            if games[9].player1.id == episode.id:
                rating_change = episode.rating - games[9].player1_pre
            else:
                rating_change = episode.rating - games[9].player2_pre
        except IndexError: #Episode has been rated fewer than 10 times
            rating_change = None
    except ObjectDoesNotExist:
        games = None
    context = {'episode': episode, 'games':games, 'rating_change':rating_change}
    return render(request, 'episode_detail.html', context)

#Displays list of episodes in season in descending rating order,
def season_detail(request, season_id):
    episodes = Episode.objects.filter(season=season_id).order_by('id')
    if not episodes: #Non-existent season, return to season rankings page
        raise Http404()
    sum = 0
    min_rating = episodes[0].rating
    max_rating = episodes[0].rating
    min_index = 0
    max_index = 0
    for index, episode in enumerate(episodes):
        if episode.rating < min_rating:
            min_rating = episode.rating
            min_index = index
        elif episode.rating > max_rating:
            max_rating = episode.rating
            max_index = index
        sum += episode.rating
    average = round(sum/episodes.count(), 1)
    context = {'episodes':episodes, 'average_rating':average, 'season': season_id, 'best_episode':episodes[max_index],
               'worst_episode':episodes[min_index]}
    return render(request, 'season_detail.html', context )

#Helper method to generate random episode IDs
def get_episodes():
    total_episodes = Episode.objects.count()
    episode_1 = random.randint(0, total_episodes - 1)
    episode_2 = random.randint(0, total_episodes - 1)
    while episode_1 == episode_2: #ensures random
        episode_2 = random.randint(0, total_episodes - 1)

    return episode_1, episode_2

#Helper method for updating slugs--only needed for updating existing database as new databases will have slugs upon creation
def update_slugs():
    for episode in Episode.objects.all():
        episode.save()

#Helper method for adding game deltas--only need for updating existing database
def update_games():
    for game in Game.objects.all():
        game.player1_delta = game.player1_post - game.player1_pre
        game.player2_delta = game.player2_post - game.player2_pre
        game.save()


