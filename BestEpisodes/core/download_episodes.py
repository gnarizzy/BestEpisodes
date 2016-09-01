#A script to download all episode data and load it into the database
import requests
from core.models import Episode


#Fetches number of seasons for series
response = requests.get('http://www.omdbapi.com/?t=The%20Simpsons').json()
seasons = int(response['totalSeasons'])


def download():
    for season in range(seasons):
        season_url = 'http://www.omdbapi.com/?t=The%20Simpsons&Season=' + str(season + 1)
        season_data = requests.get(season_url).json()
        num_episodes = len(season_data['Episodes'])

        for episode in range(num_episodes):
           episode_data = requests.get(season_url + '&Episode=' + str(episode + 1)).json()

           new_episode = Episode()
           new_episode.imdb_id = episode_data['imdbID']
           new_episode.series = season_data['Title']
           new_episode.season = season + 1
           new_episode.episode = int(episode_data['Episode'])
           new_episode.title = episode_data['Title']
           new_episode.plot = episode_data['Plot']
           new_episode.image = episode_data['Poster']
           new_episode.rating = 1000
           new_episode.save()













#Improvements down the road: test suite for script, pass in series in command line, add error handling, paramaters for
#downloading specific seasons, episodes, series, output as it's in progress