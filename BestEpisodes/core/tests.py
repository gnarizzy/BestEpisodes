from django.test import TestCase
from django.core.urlresolvers import resolve
from core.views import home
from core.models import Episode


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_episodes_loaded_into_database_correctly(self):
        episode = Episode.objects.filter(imdb_id="tt0756399")
        self.assertIsNot(episode.count(), 0)
        self.assertEqual(episode.series, "The Simpsons")
        self.assertEqual(episode.season, 1)
        self.assertEqual(episode.episode, 4)
        self.assertEqual(episode.title, "There's No Disgrace Like Home")
        self.assertEqual(episode.plot("After being embarrassed by the rest of the family at a company picnic, Homer "
                                      "becomes obsessed with improving their behavior towards each other."))
        self.assertEqual(episode.image, "http://ia.media-imdb.com/images/M/MV5BNzMwODQzMTQ4N15BMl5BanBnXkFtZTgwODU1NjQ2M"
                                        "jE@._V1_SX300.jpg")

        episode_2 = Episode.objects.filter(imdb_id="tt5222750")
        self.assertIsNot(episode_2.count(), 0)
        self.assertEqual(episode_2.series, "The Simpsons")
        self.assertEqual(episode_2.season, 27)
        self.assertEqual(episode_2.episode, 20)
        self.assertEqual(episode_2.title, "To Courier with Love")
        self.assertEqual(episode_2.plot("After promising Marge the trip of a lifetime, Homer makes a deal with a travel "
                                      "agent to be a courier of a top-secret briefcase in exchange for a discounted "
                                      "family vacation to Paris."))
        self.assertEqual(episode_2.image, "http://ia.media-imdb.com/images/M/MV5BMjI5NDYyMjUyNl5BMl5BanBnXkFtZTgwOTAxNjY"
                                          "4ODE@._V1_UY268_CR87,0,182,268_AL_.jpg")



#Test that episodes are loaded into database correctly

#Test that episodes are selected randomly

#Test that ratings are updated correctly in the case of a win

#Test that ratings are updated correctly in the case of a draw

#Test that ratings aren't updated if user selects pass

#Test that redirect occurs after submission

#Test that previous selection confirmation appears after redirect

#Test for rankings

#Test for episode detail page

#test deltas for games

#rating history tests

#test rating change over last 10 games is correct






