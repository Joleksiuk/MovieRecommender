from django.contrib import admin

from .models import Room, Topic, Message, Genre, Company

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Genre)
admin.site.register(Company)
