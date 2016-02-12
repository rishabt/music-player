import unittest
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from music_app.views import newroom

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_response_newroom(self):
        """Test for redirection on newroom"""
        response = self.client.get(reverse('create a room'))
        self.assertEqual(response.status_code,302)

    def test_roomURL(self):
        """test for successful follow"""
        response = self.client.get(reverse('create a room'), follow = True)
        self.assertEqual(response.status_code,200)

    def test_room(self):
        """Test of response url is valid"""
        response = self.client.get(reverse('create a room'), follow = True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.templates[0].name, 'party_room.html')
        self.assertEqual(response.resolver_match.func, newroom)

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.templates[0].name, 'index.html')
