from django.shortcuts import render
from django.http import HttpResponseRedirect
from core.models import Episode
import random

# Shows two unique, randomly selected episodes with screenshot, title, and description
def home(request):

    #User made a selection
    if request.method == 'POST':
        print ('POST!')
        if "episode-1-selected" in request.POST:
            print("episode 1 is the winner")
            return HttpResponseRedirect('/episode1')

        elif "episode-2-selected" in request.POST:
            print("episode 2 is the winner")
            return HttpResponseRedirect('/episode2')
        elif "draw" in request.POST:
            print("It's a draw")
            return HttpResponseRedirect('/draw')

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



