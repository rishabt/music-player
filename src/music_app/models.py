from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Room(models.Model):
    room_id = models.IntegerField(max_length=5)
    song_limit = models.IntegerField(default=3)

    def __str__(self):
        return str(self.room_id)

@python_2_unicode_compatible
class Song(models.Model):
    link = models.CharField(max_length=44)
    add_time = models.DateTimeField("time song was added")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #user_ip = models.CharField(max_length=45)

    #print "%s -- %s" % (title, author)
    def __str__(self):
        return self.link

@python_2_unicode_compatible
class History(models.Model):
    link = models.CharField(max_length=44)
    add_time = models.DateTimeField("time song was added")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #user_ip = models.CharField(max_length=45)

    #print "%s -- %s" % (title, author)
    def __str__(self):
        return self.link

@python_2_unicode_compatible
class User(models.Model):
    ip_address = models.PositiveIntegerField(max_length=12)
    songs_added = models.PositiveIntegerField(max_length=3)
    status = models.CharField(max_length=1)
    def __str__(self):
        return str(self.ip_address)
