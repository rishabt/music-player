from django.test import TestCase
from music_app.models import Room
from music_app.models import Song

class RoomTestCase(TestCase):

    def testStr(self):
        """Currently tests the max length of the ID field"""
        testRoom = Room()
        roomLen = len(str(testRoom))
        maxlenpass = (roomLen <= 5)
        self.assertTrue(maxlenpass)

class SongTestCase(TestCase):

    def testStr(self):
        testSong = Song()
        linkLen = len(str(testSong))
        maxlenpass = (linkLen <= 44)
        self.assertTrue(maxlenpass)
