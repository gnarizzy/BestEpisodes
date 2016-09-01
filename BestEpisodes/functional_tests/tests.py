from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    #Homer goes to a cool website to compare Simpsons episodes. When he arrives on the home page, he notices the title
    #Rate The Simpsons (any better title ideas?)
    def test_home_page_renders_correctly(self):
        self.browser.get(self.live_server_url)
        title = self.browser.find_element_by_tag_name('title')
        self.assertIn(title, 'Rate The Simpsons')
        first_episode = self.browser.find_element_by_id("id_episode_1")
        second_episode = self.browser.find_element_by_id("id_episode_2")
        self.assertIsNotNone(first_episode)
        self.assertIsNotNone(second_episode)

    #He is immediately prompted with two episodes to rate. Each episode has an image, a title and description.


#He prefers the episode on the left. Upon clicking its image, the page refreshes with two new episodes to compare.

#Each episode again has an image, a title, and a description. This time he prefers the episode on the right. Once again,
#the page refreshes and two new episodes are presented.

#This time he chooses "tie" and two new episodes are presented.

#This time he chooses "skip" and two new episodes are presented.

#He eventually clicks "top episodes" to see the best episodes. They are rated in descending order.

#Satisfied, he leaves the site to pay a visit to Lard Lad Donuts.

#test CSS loads