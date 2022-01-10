from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic, Genre, Company, Movie, Profile
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Message
import pandas as p
from ast import literal_eval
import random as rand
import requests
import json


def movie(request, pk):

    movie = Movie.objects.get(id=pk)
    poster_url = get_poster_url(movie.movie_id)
    result = 'https://image.tmdb.org/t/p/original' + poster_url
    movie.poster_path=result

    genres_dic = get_api_value(movie.movie_id, 'genres')
    genres =[]
    for x in range(0, len(genres_dic)):
        genres.append(genres_dic[x]['name'])

    companies_dic = get_api_value(movie.movie_id, 'production_companies')
    companies=[]
    for x in range(0, len(companies_dic)):
        companies.append(companies_dic[x]['name'])

    context={'movie': movie, 'genres': genres, 'companies': companies}
    return render(request,"MovieRecommender/movie.html", context)


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
    return str(parse_json['poster_path'])


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user_id=user)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    fav_movies = profile.fav_movies.all()
    for x in fav_movies:
        x.poster_path = 'https://image.tmdb.org/t/p/original' + get_poster_url(x.movie_id)
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'profile': profile, 'fav_movies': fav_movies}
    return render(request, 'MovieRecommender/profile.html', context)


def addToFavourites(request, pk):
    print('siema ', pk)
    movie = Movie.objects.get(movie_id=pk)
    user = request.user
    profile = Profile.objects.get(user_id=user)
    profile.fav_movies.add(movie)
    return redirect('movie', movie.id)


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

    i = 0

    for x in range(495,Movie.objects.all().count()):
        movie = Movie.objects.get(id=x)
        movie.poster_path = 'https://image.tmdb.org/t/p/original'+get_poster_url(movie.movie_id)
        movie.title = get_api_value(movie.movie_id, 'title')

        genres = get_api_value(movie.movie_id,'genres')
        for x in genres:
            movie.genres.add(Genre.objects.get(genre_id=x['id']))

        i = i + 1
        print(i)
        #companies = get_api_value(movie.movie_id,'production_companies')
        #for y in companies:
        #    #movie.production_companies.add(Company.objects.get(company_id = y['id']))
        #    print(y['id'], " ", y['name'])


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


