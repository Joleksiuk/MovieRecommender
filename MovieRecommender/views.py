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

    try: rating = Rating.objects.get(movie = movie,user = request.user)
    except: rating = 'Not rated'

    context={'movie': movie, 'genres': genres, 'companies': companies, 'rating':rating}
    return render(request,"MovieRecommender/movie.html", context)


def get_api_value(movie_id, value):
    api = 'https://api.themoviedb.org/3/movie/' + str(
        movie_id) + '?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(str(data))
    return parse_json[value]

@csrf_exempt
def rate_movie(request):
    data = json.loads(request.body)
    movie_id = data['movie_id']
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        movie = None

    rating_value = data['value']
    user = request.user
    print(data)
    print('Movie: ', movie, " User: ", user, ' Rating: ', rating_value)

    try:
        rating = Rating.objects.get(user= user,movie=movie)
    except:
        rating = None

    if rating is not None:
        print('Updated')
        rating.value=rating_value
        rating.save()
    else:
        print('Created')
        Rating.objects.create(
            movie=movie,
            value=rating_value,
            user=user
        )

    response = HttpResponse(request)
    response.status_code = 200
    return response


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
    df = p.read_csv('E:/PythonProjects/data/rate2.csv')
    column_names = ['user_id', 'movie_id', 'rating']
    data = df[column_names]

    for x in range(0, len(data)):
        print(data.iloc[x]['user_id'], "", data.iloc[x]['movie_id'], "", data.iloc[x]['rating'])

        if data.iloc[x]['user_id'] != 5 & data.iloc[x]['user_id'] != 6 & data.iloc[x]['user_id'] != 7:
            user = User.objects.get(id=data.iloc[x]['user_id'])
            movie = Movie.objects.get(id=data.iloc[x]['movie_id'])
            value = data.iloc[x]['rating']
            Rating.objects.create(
                user=user,
                movie=movie,
                value=value
            )
        print(user,"",  movie, "",value)


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


