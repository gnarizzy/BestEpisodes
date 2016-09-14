#A script to download all episode data and load it into the database
import requests, shutil
from core.models import Episode


#Fetches number of seasons for series
response = requests.get('http://www.omdbapi.com/?t=The%20Simpsons').json()
seasons = int(response['totalSeasons'])


def download():
    print("download has begun")
    for season in range(seasons):
        print("now downloading season " + str(season + 1))
        season_url = 'http://www.omdbapi.com/?t=The%Office&Season=' + str(season + 1)
        season_data = requests.get(season_url).json()
        num_episodes = len(season_data['Episodes'])

        for episode in range(num_episodes):
           try:
                episode_data = requests.get(season_url + '&Episode=' + str(episode + 1)).json()
                new_episode = Episode()
                new_episode.imdb_id = episode_data['imdbID']
                new_episode.series = season_data['Title']
                new_episode.season = season + 1
                new_episode.episode = int(episode_data['Episode'])
                new_episode.title = episode_data['Title']
                new_episode.plot = episode_data['Plot']
                new_episode.image_src = episode_data['Poster']
                new_episode.rating = 1000

                response = requests.get(episode_data['Poster'], stream=True)
                with open('static/images/S'+str(season + 1)+'E'+str(episode + 1)+'.jpg', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                new_episode.image = '../static/images/S'+str(season + 1)+'E'+str(episode + 1)+'.jpg'

                new_episode.save()

                print("Just completed S" +str(season + 1)+"E"+str(episode + 1))

           except:
               log = open('log.txt', 'w')
               log.write('Exception occurred on Season ' + str(season + 1) + ' episode ' + str(episode + 1))
               print('Exception occurred on Season ' + str(season + 1) + ' episode ' + str(episode + 1))
               continue
















#Improvements down the road: test suite for script, pass in series in command line, add error handling, paramaters for
#downloading specific seasons, episodes, series, output as it's in progress