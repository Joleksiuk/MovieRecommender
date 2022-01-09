from django.contrib import admin

from .models import Room, Topic, Message, Genre, Company, Movie, Profile

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Genre)
admin.site.register(Company)
admin.site.register(Movie)
admin.site.register(Profile)
