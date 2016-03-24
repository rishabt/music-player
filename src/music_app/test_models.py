from django.test import TestCase
from music_app.models import Room
from music_app.models import Song
from music_app.models import User
from datetime import datetime
from django.db import IntegrityError


class RoomTestCase(TestCase):

    def testStr(self):
        """Currently tests the max length of the ID field"""
        testRoom = Room()
        roomLen = len(str(testRoom))
        maxlenpass = (roomLen <= 5)
        self.assertTrue(maxlenpass)

    def testDefault(self):
        testRoom = Room()
        lim = testRoom.song_limit
        self.assertTrue(lim == 3)

    def testFail(self):
        """Impossible to create room with string ID"""
        testRoom = Room(room_id="Hello")
        self.assertRaises(ValueError,testRoom.save)


class SongTestCase(TestCase):

    def testStr(self):
        testSong = Song()
        linkLen = len(str(testSong))
        maxlenpass = (linkLen <= 44)
        self.assertTrue(maxlenpass)

    def test_link(self):
        s = Song(link="TestlinkLength",add_time=datetime.now())
        #s.save()
        self.assert_(True)

        s2 = Song(link="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.assertTrue(len(s2.link) >= 44)


    def test_add_time(self):
        d = datetime.now()
        s = Song(add_time=d)
        self.assertTrue(d == s.add_time)


    def test_room(self):
        r = Room(room_id=1234)
        r.save()

        s = Song(room=r)
        #s.save()
        self.assertEqual(str(s.room),str(r.room_id))

class UserTestCase(TestCase):

    def test_ip(self):
        u = User(ip_address = -100,songs_added = 0)
        self.assertRaises(ValueError,u.save())

    def test_songs_added(self):
        u = User(ip_address = 100,songs_added = 10000)
        self.assertRaises(ValueError,u.save())
    def test_status(self):
        u = User(ip_address = 100,songs_added = 10000, status = "OK")
        self.assertRaises(ValueError,u.save())
