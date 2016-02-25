from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from django.template import RequestContext
from random import randint
from music_app.models import Room, Song, User
from django.utils import timezone
from django.core.urlresolvers import reverse


DEVELOPER_KEY = "AIzaSyD8HURVZ1FujOXAK1NzoNHceCZYL6OLBzg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
    return render_to_response('index.html', context_instance=RequestContext(request))

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


        return render_to_response("party_room.html", {"response_message": videos_returned, "song_list": song_list})

    # if the user hasn't entered anything in the search bar, just do nothing
    return render(request, "party_room.html", {"song_list": song_list})

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

    new_room = Room(room_id=id)
    new_room.save()
    return HttpResponseRedirect(reverse('room', args=(id,client_ip)))

def check_room_exists(request):
  id = request.GET['room_id']
  response_data = {}
  response_data['response'] = True
  if Room.objects.filter(room_id = id).exists():
    return JsonResponse({"RESPONSE" : True})
  else
    return JsonResponse({"RESPONSE" : False})

def guest_joins_room(request):

  #yo Deepak, this has to be changed to the actual room id
  id = 71971


  ip_address = get_client_ip(request)
  client_ip = ip_address.replace('.','')
  return HttpResponseRedirect(reverse('room', args=(id,client_ip,)))



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def set_song_limit(request):
  return render_to_response('index.html', context_instance=RequestContext(request))

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
