from django.db import models
from django.contrib.auth.models import User
# make class (query) ->  python manage.py makemigrations -> python manage.py migrate
# admin.py -> from .models import className -> admin.site.register(className)

# id is generated as primary key automatically
# auto_now passed as an argument saves captures time of every CRUD action
# auto_now_add passed as an argument captures time of creating a query


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User,related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Genre(models.Model):
    genre_id = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("genre_id", "name"),)


class Company(models.Model):
    company_id = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)
    overview = models.TextField()
    budget = models.FloatField()

    genres = models.ManyToManyField(Genre, related_name="genres", blank=True)
    production_companies = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    org_language = models.CharField(max_length=200)
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=200)
    release_date = models.CharField(max_length=200)
    video = models.CharField(max_length=200)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

    def __str__(self):
        return self.title



