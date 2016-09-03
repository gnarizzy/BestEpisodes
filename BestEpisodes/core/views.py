from django.shortcuts import render
from django.http import HttpResponseRedirect
from core.models import Episode, Game
from core.calculator import calculate
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
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')

        elif "episode-2-selected" in request.POST:
            episode1 = Episode.objects.filter(title=request.POST['first_episode_title'])[0]
            episode2 = Episode.objects.filter(title=request.POST['second_episode_title'])[0]
            new_rating1, new_rating2 = calculate(episode1.rating, episode2.rating, 0)
            game = Game.objects.create(player1=episode1, player2=episode2, result=0, player1_pre=episode1.rating,
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')
        elif "draw" in request.POST:
            episode1 = Episode.objects.filter(title=request.POST['first_episode_title'])[0]
            episode2 = Episode.objects.filter(title=request.POST['second_episode_title'])[0]
            new_rating1, new_rating2 = calculate(episode1.rating, episode2.rating, 0.5)
            game = Game.objects.create(player1=episode1, player2=episode2, result=0.5, player1_pre=episode1.rating,
                                       player1_post=new_rating1, player2_pre=episode2.rating, player2_post=new_rating2)
            episode1.rating, episode2.rating = new_rating1, new_rating2
            episode1.save()
            episode2.save()
            return HttpResponseRedirect('/')

    #skipped, redirected, or coming to home page
    episodeid_1, episodeid_2 = get_episodes()
    first_episode = Episode.objects.all()[episodeid_1]
    second_episode = Episode.objects.all()[episodeid_2]
    context = {'first_episode': first_episode, 'second_episode':second_episode}

    return render(request, 'home.html', context)

#Helper method to generate random episode IDs
def get_episodes():
    total_episodes = Episode.objects.all().count()
    episode_1 = random.randint(0, total_episodes - 1)
    episode_2 = random.randint(0, total_episodes - 1)
    while episode_1 == episode_2: #ensures random
        episode_2 = random.randint(0, total_episodes - 1)

    return episode_1, episode_2



