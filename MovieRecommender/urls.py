from django.urls import path
from . import views
from . my_views import home_views
from . my_views import login_views
from . my_views import room_views

urlpatterns = [
    path('login/', login_views.loginPage, name='login'),
    path('logout/', login_views.logoutUser, name='logout'),
    path('register/', login_views.registerPage, name='register'),

    path('', home_views.home, name='home'),
    path('room/<str:pk>', room_views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),

    path('create-room/', room_views.createRoom, name="create-room"),
    path('update-room/<str:pk>', room_views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', room_views.deleteRoom, name="delete-room"),


    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),

    path('read-data/', views.readData, name='read-data'),

    path('movie=<str:pk>', views.movie, name='movie'),

    path('add-favourite/<str:pk>', views.addToFavourites, name='add-favourite'),

    path('rate-movie/', views.rate_movie, name='rate-movie')
]
