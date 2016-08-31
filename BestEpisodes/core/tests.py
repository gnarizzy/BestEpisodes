from django.test import TestCase
from django.core.urlresolvers import resolve
from core.views import home
from django.http import HttpRequest


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


#Test that episodes are loaded into database correctly

#Test that episodes are selected randomly

#Test that ratings are updated correctly in the case of a win

#Test that ratings are updated correctly in the case of a draw

#Test that ratings aren't updated if user selects pass








