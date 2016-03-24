import unittest
from django.test import Client
from time import sleep
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from music_app.views import newroom
from music_app.views import room
from music_app.views import home
from music_app.views import youtube_search
from music_app.views import add_song
from music_app.views import Guest_Joins_Room
from music_app.views import RemoveMusic
from music_app.views import PlaySongView
from music_app.views import GetHistoryView
from music_app.views import UpdateQueueView
from music_app.views import IdentifyUserView
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

    def test_remove_music(self):
        """Test removes music function call"""
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        removeurl = base + "remove/"
        response = self.client.post(removeurl,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.resolver_match.func, RemoveMusic)

    def test_remove_music_response(self):
        """Test removes music response code"""
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        removeurl = base + "remove/"
        response = self.client.post(removeurl,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        print(removeurl)
        self.assertEqual(response.status_code, 302)

    def test_remove_music_faliure(self):
        """Test removes music faliure"""
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        removeurl = base + "remove/"
        response = self.client.post(removeurl,{'link':'https://www.youtube.asdasdasdasd/embed/YQHsXMglC9A'})
        print(removeurl)
        self.assertEqual(response.status_code, 302)

    def test_play_song(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        playurl = base + "playsong/"
        response = self.client.post(playurl,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.resolver_match.func, PlaySongView)

    def test_play_song_response(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        playurl = base + "playsong/"
        response = self.client.post(playurl,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 200)

    def test_play_song_faliure(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        playurl = base + "playsong/"
        response = self.client.post(playurl,{'link':'https://www.youtube.com/embed/YQHasdasdasdadadawsdawdawsdasdsXMglC9A'})
        self.assertEqual(response.status_code, 200)

    def test_get_history(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        histurl = base + "history/"
        response = self.client.get(histurl)
        self.assertEqual(response.resolver_match.func, GetHistoryView)

    def test_get_history_response(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        histurl = base + "history/"
        response = self.client.get(histurl)
        self.assertEqual(response.status_code,200)

    def test_get_history_fail(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-10]
        histurl = base + "2342/history/"
        response = self.client.get(histurl)
        self.assertEqual(response.status_code,404)

    def test_update_queue_function(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        queueurl = base + "queue/"
        response = self.client.get(queueurl)
        self.assertEqual(response.resolver_match.func, UpdateQueueView)

    def test_update_queue_response(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-7]
        queueurl = base + "queue/"
        response = self.client.get(queueurl)
        self.assertEqual(response.status_code, 200)

    def test_update_queue_response(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        newURL = base + "addsong/"
        response = self.client.post(newURL,{'link':'https://www.youtube.com/embed/YQHsXMglC9A'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, add_song)
        base = base[:-10]
        queueurl = base + "2342/queue/"
        response = self.client.get(queueurl)
        self.assertEqual(response.status_code,404)

    def test_ID_func(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        base = base[:-14]
        selfurl = base + "/user/status"
        print(selfurl)
        response = self.client.get(selfurl)
        self.assertEqual(response.resolver_match.func, IdentifyUserView)

    def test_ID_response(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        base = base[:-14]
        selfurl = base + "/user/status"
        print(selfurl)
        response = self.client.get(selfurl)
        self.assertEqual(response.status_code, 200)

    def test_ID_fail(self):
        response = self.client.get(reverse('create a room'), follow = True)
        base = response.request["PATH_INFO"]
        base = base[:-14]
        selfurl = base + "/user/sttus"
        response = self.client.get(selfurl)
        self.assertEqual(response.status_code, 404)
