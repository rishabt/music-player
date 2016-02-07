from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core import serializers
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


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



#the main view
def index(request):

    videos_returned = []

    #get the query element and send it to the search youtube method, then send the results to the array
    if request.method == 'GET' and request.GET.get("query_element") :
        youtube_query = request.GET.get("query_element")

        try:
          youtube_search(youtube_query, videos_returned)
        except HttpError, e:
          print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


        return render_to_response("index.html", {"response_message": videos_returned})

    # if the user hasn't entered anything in the search bar, just do nothing
    return render(request, "index.html", {})