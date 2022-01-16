from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Room, Topic, Genre, Company, Movie, Profile, Rating, Actor
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


def get_actor_movies_from_API(actor_id):
    api_path = 'https://api.themoviedb.org/3/person/' + str(actor_id) + '/credits?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US '
    response_API = requests.get(api_path)

    api_text = response_API.text
    data = json.loads(api_text)

    movie_list =[]

    for x in range(0, len(data['cast'])):
        poster_path = str(data['cast'][x]['poster_path'])
        if poster_path != 'None':
            full_path = 'https://image.tmdb.org/t/p/original' + str(poster_path)
        else:
            full_path = 'https://www.scifi-movies.com/images/site/en/affiche_nondisponible.jpg'

        movie_list.append(Movie.objects.create(
            movie_id=data['cast'][x]['id'],
            title=data['cast'][x]['title'],
            poster_path=full_path
        ))

    return movie_list


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
    api = 'https://api.themoviedb.org/3/movie/' + str(
        movie_id) + '?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(str(data))
    try:
        pp = parse_json['poster_path']
    except:
        pp = None

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


def get_actor_from_API(actor_id):
    api_path = 'https://api.themoviedb.org/3/person/' + str(actor_id) + '?api_key=4b5f9777a2d363363cbb7d26017f0052' \
                                                                        '&language=en-US '
    response_API = requests.get(api_path)
    api_text = response_API.text
    data = json.loads(api_text)
    path = str(data['profile_path'])

    if path == 'None':
        full_path = "https://davinci22.ru/wp-content/uploads/2014/01/default-avatar-m_1920.png"
    else:
        full_path = 'https://image.tmdb.org/t/p/original'+path

    actor = Actor.objects.create(
        actor_id=actor_id,
        name=data['name'],
        biography=data['biography'],
        popularity=data['popularity'],
        profile_path=full_path,
    )
    return actor


def get_movie_from_API(movie_id):

    api_path = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key=4b5f9777a2d363363cbb7d26017f0052'
    response_API = requests.get(api_path)
    api_text = response_API.text
    data = json.loads(api_text)
    movie = None
    if len(data)==25:
        poster_path = str(data['poster_path'])
        if poster_path != 'None':
            full_path = 'https://image.tmdb.org/t/p/original' + str(poster_path)
        else:
            full_path = 'https://www.scifi-movies.com/images/site/en/affiche_nondisponible.jpg'

        companies = []
        #for x in range(0,len(data['production_companies'])):
        #   companies.append(Company.objects.get(company_id=data['production_companies'][x]['id']))
        genres = []

        for x in range(0, len(data['genres'])):
            genres.append(Genre.objects.get(genre_id=data['genres'][x]['id']))

        movie = Movie.objects.create(
            movie_id=data['id'],
            title=data['title'],
            overview=data['overview'],
            vote_count=data['vote_count'],
            vote_average=data['vote_average'],
            poster_path=full_path
        )

        for x in genres:
            movie.genres.add(x)
        for x in companies:
            movie.production_companies.add(x)

    return movie


def get_cast_from_API(movie_id):
    api_path = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key' \
                                                                       '=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api_path)
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json


def readData(request):
    data = get_cast_from_API(38348)
    cast = data['cast']
    cast_list =[]
    for x in range (0, len(cast)):
        name = cast[x]['name']
        path = 'https://image.tmdb.org/t/p/original'+ str(cast[x]['profile_path'])
        character = cast[x]['character']
        popularity = cast[x]['popularity']
        actor_id = cast[x]['id']
        actor = Actor.objects.create(
            actor_id=actor_id,
            name=name,
            profile_path=path,
            character=character,
            popularity=popularity
        )
        cast_list.append(actor)
    print(cast_list)

    context = {}
    return render(request, 'MovieRecommender/read_data.html', context)


def load_ratings():

    movies = Movie.objects.all()
    df = p.read_csv('E:/PythonProjects/data/rate10.csv')
    column_names = ['user_id', 'movie_id', 'rating']
    data = df[column_names]

    for x in range(0, len(data)):
        user_id = data.iloc[x]['user_id']
        movie_id = data.iloc[x]['movie_id']
        new_rating = data.iloc[x]['rating']
        try:
            movie = Movie.objects.get(id=movie_id)

            try:
                rating = Rating.objects.get(user_id=user_id, movie_id=movie_id)
            except:
                rating = None

            # Updating Rating
            if rating is not None:
                print('Updated')
                print('Before removing update: ', movie.vote_average, movie.vote_count)
                # Removing old rating from average rating
                if movie.vote_count != 1:
                    movie.vote_average = ((movie.vote_average * movie.vote_count) - rating.value) / (
                                movie.vote_count - 1)
                    movie.vote_count = movie.vote_count - 1
                else:
                    movie.vote_average = 0.0
                movie.save()
                print('After removing update: ', movie.vote_average, movie.vote_count)

                rating.value = new_rating
                rating.save()
                # Creating new Rating
            else:
                print('Created')
                Rating.objects.create(
                    movie=Movie.objects.get(id=movie_id),
                    value=new_rating,
                    user=User.objects.get(id=user_id),
                )
                # Adding new rating to average rating
            new_movie_rating = (movie.vote_average + new_rating) / (movie.vote_count + 1)
            movie.vote_average = round(new_movie_rating, 1)
            movie.vote_count = movie.vote_count + 1
            movie.save()
        except:
            pass


def get_top_rated_user_movies(num_of_movies, user_id):
    sql = 'SELECT id, movie_id From MovieRecommender_rating ' \
          'WHERE user_id = ' + str(user_id) + ' ORDER BY value DESC LIMIT ' + str(num_of_movies)

    movies = []
    for x in Rating.objects.raw(sql):
        movies.append(Movie.objects.get(id = x.movie_id))

    return movies


def count_frequencies(arg_list):
    result = []
    for i in set(arg_list):
        duplicateFrequencies = {'user_id': i, 'count': arg_list.count(i)}
        result.append(duplicateFrequencies)
    return result


def convert_to_df(query_name):
    dat = sqlite3.connect('db.sqlite3')
    sql = 'SELECT * From ' + query_name
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


def ipdate_movie_paths():
    movies = Movie.objects.all()

    for x in range(1, len(movies)):
        movie = Movie.objects.get(id=x)
        poster_url = str(get_poster_url(movie.movie_id))

        if poster_url != 'None':
            result = 'https://image.tmdb.org/t/p/original' + poster_url
        else:
            result = 'https://www.scifi-movies.com/images/site/en/affiche_nondisponible.jpg'
        movie.poster_path = result
        movie.save()


def get_cast_from_API(movie_id):
    api_path = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits?api_key' \
                                                                       '=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api_path)
    api_text = response_API.text
    data = json.loads(api_text)

    cast = data['cast']
    cast_list =[]
    for x in range (0, len(cast)):
        name = cast[x]['name']
        path = str(cast[x]['profile_path'])
        if path == 'None':
            full_path = "https://davinci22.ru/wp-content/uploads/2014/01/default-avatar-m_1920.png"
        else:
            full_path = 'https://image.tmdb.org/t/p/original'+ path

        character = cast[x]['character']
        popularity = cast[x]['popularity']
        actor_id = cast[x]['id']
        actor = Actor.objects.create(
            actor_id=actor_id,
            name=name,
            profile_path=full_path,
            character=character,
            popularity=popularity
        )
        cast_list.append(actor)
    return cast_list
