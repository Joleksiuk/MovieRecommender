import datetime


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
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
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


class Company(models.Model):
    company_id = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company_id", "name"),)


class Movie(models.Model):
    movie_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=200, default="")
    overview = models.TextField(default="")
    budget = models.FloatField(default=0.0)

    genres = models.ManyToManyField(Genre, related_name="genres", blank=True)

    org_language = models.CharField(max_length=200, default="")
    popularity = models.FloatField(default=0.0)
    poster_path = models.CharField(max_length=200, default="https://www.scifi-movies.com/images/site/en/affiche_nondisponible.jpg")
    release_date = models.CharField(max_length=200, default="")
    video = models.CharField(max_length=200, default="")
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    adults = models.CharField(max_length=200, default="False")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['movie_id']


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200, default="")
    picture_path = models.CharField(max_length=200, default="https://upload.wikimedia.org/wikipedia/commons/1/1e/Default-avatar.jpg")
    fav_movies = models.ManyToManyField(Movie, related_name="fav_movies", blank=True)
    sex = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return str(self.value)


class Actor(models.Model):
    actor_id=models.IntegerField(default=0.0)
    name = models.CharField(max_length=200, default="")
    role = models.CharField(max_length=200, default="")
    character = models.CharField(max_length=200, default="")
    biography = models.TextField(null=True, blank=True)
    birthday = models.CharField(max_length=200, default="")
    profile_path = models.CharField(max_length=200, default="https://davinci22.ru/wp-content/uploads/2014/01/default"
                                                            "-avatar-m_1920.png")
    popularity = models.IntegerField(default=0.0)

    def __str__(self):
        return str(self.name)