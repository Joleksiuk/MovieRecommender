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

rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn python2!'},
    {'id': 3, 'name': 'Lets learn python3!'}
]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__name__icontains=q))

    movies = []

    print(get_poster_url(8844))
    i=0
    while i <12:
        index = rand.randint(1, 1000)
        movie = Movie.objects.get(id=index)
        poster_url = get_poster_url(movie.movie_id)
        result = 'https://image.tmdb.org/t/p/original' + poster_url
        if poster_url!='None':
            movie.poster_path = result
            i=i+1
            movies.append(movie)
            print(result)




    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages,'movies': movies}

    return render(request, 'MovieRecommender/home.html', context)


def get_poster_url(movie_id):
    api = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
    response_API = requests.get(api)
    data=response_API.text
    if response_API == '200':
        print('resppoonse 200')
    parse_json = json.loads(str(data))
    return str(parse_json['poster_path'])


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'MovieRecommender/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user_id=user)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'profile': profile}
    return render(request, 'MovieRecommender/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'MovieRecommender/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'MovieRecommender/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'MovieRecommender/delete.html', {'obj': room})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password').lower()
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'MovieRecommender/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'MovieRecommender/login_register.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'MovieRecommender/delete.html', {'obj': message})


class gen:
    def __init__(self, my_id, name):
        self.my_id = my_id
        self.name = name


def readData(request):

    #for x in range(1, Movie.objects.all().count()):
     #   movie = Movie.objects.get(id=x)
     #   api = 'https://api.themoviedb.org/3/movie/'+str(movie.movie_id)+'?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US'
     #   response_API = requests.get(api)
     #   data = response_API.text
     ##   movie.poster_path = 'https://image.tmdb.org/t/p/original'+str(parse_json['poster_path'])

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


def read_movie_data():
    df = p.read_csv('E:/PythonProjects/data/movies_metadata.csv')
    column_names = ['id', 'title', 'overview', 'budget', 'original_language', 'popularity', 'poster_path',
                    'release_date', 'video'
        , 'vote_average', 'vote_count']

    data = df[column_names]

    genres_id = df['genres'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    companies_id = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    for x in range(40000, len(data)):
        print(x)
        for x in range(0, len(data)):
            movie = Movie.objects.filter(movie_id=data.iloc[x]['id'])
            for y in range(0, len(genres_id[x])):
                grn = Genre.objects.get(genre_id=genres_id[x][y])
                for z in range(0, len(movie)):
                    movie[z].genres.add(grn)

            for y in range(0, len(companies_id[x])):
                crn = Company.objects.get(company_id=companies_id[x][y])
                for z in range(0, len(movie)):
                    movie[z].production_companies.add(crn)
        print(movie)


def get_unique_values(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


def fill_genres_companies_data():
    df = p.read_csv('E:/PythonProjects/data/movies_metadata.csv')

    companies_names = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    companies_id = df['production_companies'].fillna('[]').apply(literal_eval).apply(
        lambda x: [i['id'] for i in x] if isinstance(x, list) else [])

    names = []
    i = 0
    j = 0
    for x in range(0, len(companies_names)):
        for y in range(0, len(companies_names[x])):
            names.append(companies_names[x][y])

    names = get_unique_values(names)

    ids = []
    i = 0
    j = 0
    for x in range(0, len(companies_id)):
        for y in range(0, len(companies_id[x])):
            ids.append(companies_id[x][y])

    ids = get_unique_values(ids)

    print(names)
    print(ids)

    for x in range(0, len(names)):
        Company.objects.create(company_id=ids[x], name=names[x])

    genres = df['production_companies']
