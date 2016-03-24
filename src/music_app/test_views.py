import unittest
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from music_app.views import newroom
from music_app.views import room
from music_app.views import home
from music_app.views import youtube_search
from music_app.views import add_song
from music_app.views import Guest_Joins_Room
from music_app.models import Room
from music_app.models import Song

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_response_newroom(self):
        """Test for redirection on newroom"""
        response = self.client.get(reverse('create a room'))
        self.assertEqual(response.status_code,302)

    def test_roomURL(self):
        """test for successful follow"""
        response = self.client.get(reverse('create a room'))
        self.assertEqual(response.status_code,302)
        self.assertEqual(response.resolver_match.func, newroom)

    def test_room(self):
        """Test of response url is valid"""
        response = self.client.get(reverse('create a room'), follow = True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.templates[0].name, 'party_room.html')
        self.assertEqual(response.resolver_match.func, room)

    def test_home(self):
        """Test index.html loading"""
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.templates[0].name, 'index.html')
        self.assertEqual(response.resolver_match.func, home)

    def test_youtube(self):
        """Test of youtube function being called"""
        response = self.client.get(reverse('create a room'), follow = True)
        newURL = response.request["PATH_INFO"]
        newURL = newURL + "?query_element=test"
        self.assertEqual(response.status_code, 200)

    def test_add_song(self):
        """Test of add_song func"""
        response = self.client.get(reverse('create a room'), follow = True)
        newURL = response.request["PATH_INFO"]
        newURL = newURL + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)

    def test_add_song_404(self):
        """Test ability to add songs to rooms that dont exist"""
        response = self.client.get(reverse('create a room'), follow = True)
        newURL = "/room/1744/127200/addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.resolver_match.func, add_song)

    def test_new_room(self):
        """test for successful follow"""
        response = self.client.get(reverse('create a room'))
        self.assertEqual(response.resolver_match.func, newroom)

    def test_guest_joins_room(self):
        """Test guest joins existing room"""
        response = self.client.get(reverse('join a room',kwargs={'room_id':00000}))
        self.assertEqual(response.resolver_match.func, Guest_Joins_Room)

    def test_guest_joins_room_response(self):
        """Test guest joins existing room"""
        r = Room(room_id = "12345")
        r.save()
        response = self.client.get(reverse('join a room',kwargs={'room_id':12345}), follow = True)
        self.assertEqual(response.status_code, 200)

    
