from django.shortcuts import render
from .models import Room
from django.urls import path
from django.http import HttpResponse

rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Lets learn python2!'},
    {'id': 3, 'name': 'Lets learn python3!'}
]


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'MovieRecommender/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    for i in rooms:
        if i['id'] == int(pk):
            room = i

    context = {'room': room}
    return render(request, 'MovieRecommender/room.html', context)


def createRoom(request):
    context = {}
    return render(request, 'MovieRecommender/room_form.html', context)
