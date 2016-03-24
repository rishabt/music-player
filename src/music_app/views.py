from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from django.template import RequestContext
from random import randint
from music_app.models import Room, Song, User, History
from django.utils import timezone
from django.core.urlresolvers import reverse
from .forms import SongLimitForm
from django.contrib import messages
import hashlib
import json

DEVELOPER_KEY = "AIzaSyD8HURVZ1FujOXAK1NzoNHceCZYL6OLBzg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEFAULT_SONG_LIMIT = 3

#this is not actually a view, just a method that searches youtube and returns video ids
def youtube_search(the_query, videos):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  search_response = youtube.search().list(
    q=the_query,
    part="id,snippet",
    maxResults="10"
  ).execute()

  video = []
  for search_result in search_response.get("items", []):
    video = []
    if search_result["id"]["kind"] == "youtube#video":
      video.append(search_result["snippet"]["title"])
      video.append("https://www.youtube.com/embed/" + str(search_result["id"]["videoId"]))
      video.append("http://img.youtube.com/vi/" + str(search_result["id"]["videoId"]) + "/1.jpg")
      videos.append(video)


def home(request):
    form = SongLimitForm(); # Unpopulated form
    data_dict = {'form': form}
    return render_to_response('index.html', data_dict, context_instance=RequestContext(request))

#the main view
def room(request, room_id, client_ip):
    videos_returned = []
    room = get_object_or_404(Room, room_id=room_id)
    song_list = room.song_set.order_by('add_time')

    #get the query element and send it to the search youtube method, then send the results to the array
    if request.method == 'GET' and request.GET.get("query_element") :
        youtube_query = request.GET.get("query_element")

        try:
          youtube_search(youtube_query, videos_returned)
        except HttpError, e:
          print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)



        return render(request, "party_room.html", {"response_message": videos_returned, "song_list": song_list, 'room_id':room_id, 'client_ip':client_ip})

    # if the user hasn't entered anything in the search bar, just do nothing
    return render(request, "party_room.html",  {"song_list": song_list, 'room_id':room_id, 'client_ip':client_ip})

def get_room_with_id(id):
  return Room.objects.filter(room_id = id)

def create_a_new_room(id,song_lim = DEFAULT_SONG_LIMIT):
  new_room = Room(room_id = id, song_limit = song_lim)
  new_room.save()
  return new_room

def check_room_exists(id):
  return Room.objects.filter(room_id = id).exists()

def check_if_user_exists(id):
  client_ip = id.replace('.','')
  return User.objects.filter(ip_address = client_ip)

# Returns User status
def check_user_status(id):
  user = get_object_or_404(User, ip_address=id)
  return user.status


def create_user(id):
    client_ip = id.replace('.','')

    if User.objects.filter(ip_address=client_ip).exists():

        user = User.objects.get(ip_address=client_ip)
        user.songs_added = 0
        user.status = "G"
        user.save()

    else:
        user = User(ip_address = client_ip,songs_added = 0, status = 'G')
        user.save()

    return user

def create_host(id):
    client_ip = id.replace('.','')
    if User.objects.filter(ip_address=client_ip).exists():

        user = User.objects.get(ip_address=client_ip)
        user.songs_added = 0
        user.status = "H"
        user.save()

    else:
        user = User(ip_address = client_ip,songs_added = 0, status = 'H')
        user.save()

    return user

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def getSongWithRoomAndLink(room_id,song_link):
    return Song.objects.filter(room__room_id = room_id, link = song_link)

def deleteAllSongsInRoom(room_id):
    Song.objects.filter(room__room_id = room_id).delete()

def addSongToHistory(song,party):
    new_song = party.history_set.create(link=song, add_time=timezone.now())
    new_song.save()

def newroom(request):
    ip_address = get_client_ip(request)
    client_ip = ip_address.replace('.','')
    youtube_query = "Deepak"
    videos_returned = []

    try:
      youtube_search(youtube_query, videos_returned)
    except HttpError, e:
      if e.resp.status == 403:
        return render(request, "index.html", {"error_message": "true"})
    while True:
      id = randint(00000,99999)
      if Room.objects.filter(room_id = id).exists():
        continue
      else:
        break

    limit=DEFAULT_SONG_LIMIT
    if request.method=='POST':
      form = SongLimitForm(request.POST)
      if form.is_valid():
        limit = request.POST.get('song_limit', '')

    create_a_new_room(id, song_lim=limit)
    user = create_host(ip_address)
    return HttpResponseRedirect(reverse('room', args=(id,client_ip)))

def Guest_Joins_Room(request,room_id):

  ip_address = get_client_ip(request)
  client_ip = ip_address.replace('.','')
  room = {}
  user = {}
  if(check_room_exists(room_id)):
    room = get_room_with_id(room_id)
    user = create_user(ip_address)
  else:
    messages.add_message(request, messages.INFO, "Room not found")
    return HttpResponseRedirect(reverse('home'))

  # add user to room
  return HttpResponseRedirect(reverse('room', args=(room_id,client_ip,)))

def Check_Room_Exists(request):
  response_data = {}
  response_data['response'] = True
  if check_room_exists(request.GET['room_id']):
    return JsonResponse({"RESPONSE" : True})
  else:
    return JsonResponse({"RESPONSE" : False})


def RemoveMusic(request, room_id):
  song_link = request.POST['link']
  song = getSongWithRoomAndLink(room_id, song_link)
  ip_address = get_client_ip(request)
  client_ip = ip_address.replace('.','')
  song.delete()
  return HttpResponseRedirect(reverse('room',args=(room_id,client_ip)))

def IdentifyUserView(request):
  ip_address = get_client_ip(request)
  client_ip = ip_address.replace('.','')
  status = check_user_status(client_ip)
  return JsonResponse({"STATUS" : status})

def get_song_limit(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

def add_song(request, room_id, client_ip):
    party = get_object_or_404(Room, room_id=room_id)
    user = get_object_or_404(User, ip_address=client_ip)
    msg = ""
    dups = int(request.POST['dups'])

    if ((dups ==1) or (check_song_in_queue(request, room_id) == 0)):
      if user.status=="H":
          new_song = party.song_set.create(link=request.POST['link'], add_time=timezone.now())
          new_song.save()
          msg = "Song Added"

      elif (user.songs_added<party.song_limit):
          new_song = party.song_set.create(link=request.POST['link'], add_time=timezone.now())
          new_song.save()
          user.songs_added += 1
          user.save()
          msg = "Song Added"

      else:
          msg = "Song limit reached"
    else:
      msg = "Song already in queue bro"

    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse('room', args=(room_id, client_ip)))
  
def PlaySongView(request, room_id):
  party = get_object_or_404(Room, room_id=room_id)
  song = request.POST['link']
  addSongToHistory(song,party)
  msg = "Song Added To History"
  messages.add_message(request, messages.INFO, msg)
  return JsonResponse({'RESPONSE': song + 'Added successfully'})

def GetHistoryView(request,room_id):
  room = get_object_or_404(Room, room_id=room_id)
  history_list = room.history_set.all()
  data = serializers.serialize("json", history_list)
  l = json.loads(data)
  history_all = [li['fields']['link'] for li in l]
  history = json.dumps(history_all)
  return JsonResponse({'history': history})

def UpdateQueueView(request, room_id):
  deleteAllSongsInRoom(room_id)
  list = request.POST.get('list', False)

  party = get_object_or_404(Room, room_id=room_id)
  for i in list:
    new_song = party.song_set.create(link=i, add_time=timezone.now())
    new_song.save()


def check_song_in_queue(request, room_id, ):
  song_link = request.POST['link']
  song = getSongWithRoomAndLink(room_id, song_link)
  if not song:
    return 0
  else:
    return 1

# def room(request, room_id, play_link=''):
    # room = get_object_or_404(Room, room_id=room_id)
    # song_list = room.song_set.order_by('add_time')
    # context = {'room_id': room_id, 'song_list': song_list, 'play_link':play_link}
    # return render(request, 'index2.html', context)

# def play_song(request, party_id):
#     party = get_object_or_404(Party, party_id=party_id)
#     song = party.song_set.all()[0]
#     song.delete()
#     return HttpResponseRedirect(reverse('playlist:detail',kwargs={'party_id':party_id}))

# def add_song(request, party_id):
#     party = get_object_or_404(Party, party_id=party_id)
#     try:
#         new_song = party.song_set.create(link=request.POST['link'], add_time=timezone.now())
#     except :
#         return render(request, 'playlist/detail.html', {
#             'party_id': party_id,
#             'song_list': party.song_set.order_by('add_time'),
#             'error_message': "Invalid Link",
#         })
#     else:
#         new_song.save()

#         return HttpResponseRedirect(reverse('playlist:detail', args=(party_id,)))
