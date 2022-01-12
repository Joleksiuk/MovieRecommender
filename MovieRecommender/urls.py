from django.urls import path
from . import views
from . my_views import home_views
from . my_views import login_views
from . my_views import room_views
from . my_views import movie_views
from . my_views import profile_views
from . my_views import recommendation_views

urlpatterns = [
    path('login/', login_views.loginPage, name='login'),
    path('logout/', login_views.logoutUser, name='logout'),
    path('register/', login_views.registerPage, name='register'),

    path('', home_views.home, name='home'),
    path('room/<str:pk>', room_views.room, name='room'),
    path('profile/<str:pk>', profile_views.userProfile, name="user-profile"),

    path('create-room/', room_views.createRoom, name="create-room"),
    path('update-room/<str:pk>', room_views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', room_views.deleteRoom, name="delete-room"),


    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('read-data/', views.readData, name='read-data'),


    path('movie=<str:pk>',  movie_views.movie, name='movie'),
    path('add-favourite/<str:pk>', movie_views.addToFavourites, name='add-favourite'),
    path('rate-movie/', movie_views.rate_movie, name='rate-movie'),
    path('rating-recommendation/', recommendation_views.rating_recommendation, name='rating-recommendation')
]
