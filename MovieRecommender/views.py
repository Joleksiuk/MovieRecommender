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
import sqlite3


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

    context = {}
    return render(request, 'MovieRecommender/read_data.html', context)


def convert_to_df(query_name):
    dat = sqlite3.connect('db.sqlite3')
    sql = 'SELECT * From '+query_name
    query = dat.execute(sql)
    cols = [column[0] for column in query.description]
    df = p.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return df


def load_profiles():
    print(Movie.objects.all().count())
    print(User.objects.all().count())
    df = p.read_csv('E:/PythonProjects/data/fav_movies.csv')
    column_names = ['user_id', 'movie_id']
    data = df[column_names]

    for x in range(0, len(data)):

        try:
            movie = Movie.objects.get(id=data.iloc[x]['movie_id'])
            user = User.objects.get(id=data.iloc[x]['user_id'])
            profile = Profile.objects.get(user_id=user)
            profile.fav_movies.add(movie)
            profile.save()
            print(user, " ", movie)
        except:
            pass



