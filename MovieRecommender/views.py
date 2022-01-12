from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic, Genre, Company, Movie, Profile, Rating
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Message
import pandas as p
from ast import literal_eval
import random as rand
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import requests
import json


def get_api_value(movie_id, value):
    api = 'https://api.themoviedb.org/3/movie/' + str(
        movie_id) + '?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(str(data))
    return parse_json[value]


def get_movie_genres(movie_id):
    api = 'https://api.themoviedb.org/3/movie/' + str(
        movie_id) + '?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(str(data))
    return parse_json['genres']


def get_poster_url(movie_id):
    api = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data=response_API.text
    parse_json = json.loads(str(data))
    try:
        pp = parse_json['poster_path']
    except:
        pp= None

    return pp



@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'MovieRecommender/delete.html', {'obj': message})


def readData(request):
    df = p.read_csv('E:/PythonProjects/data/rate2.csv')
    column_names = ['user_id', 'movie_id', 'rating']
    data = df[column_names]

    for x in range(0, len(data)):

        if data.iloc[x]['user_id'] != 5 & data.iloc[x]['user_id'] != 6 & data.iloc[x]['user_id'] != 7:
            user = User.objects.get(id=data.iloc[x]['user_id'])
            movie = Movie.objects.get(id=data.iloc[x]['movie_id'])
            value = data.iloc[x]['rating']
            Rating.objects.create(
                user=user,
                movie=movie,
                value=value
            )

    context = {}
    return render(request, 'MovieRecommender/read_data.html', context)


def load_profiles():
    df = p.read_csv('E:/PythonProjects/data/names.csv')
    column_names = ['name', 'lastname', 'email', 'birth_date', 'image_path', 'sex', 'password']
    data = df
    for x in range(0, len(data)):
        st = data.iloc[x]['name'] + " " + data.iloc[x]['lastname']
        user = User.objects.get(username=st)

        Profile.objects.create(
            user_id=user,
            name=user.username,
            picture_path=data.iloc[x]['image_path'],
            birth_date=data.iloc[x]['birth_date'],
            sex=data.iloc[x]['sex']
        )

    print(data)
    context = {'data': data}


