from MovieRecommender.views import *


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user_id=user)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    fav_movies = profile.fav_movies.all()
    for x in fav_movies:
        poster_url=str(get_poster_url(x.movie_id))
        if poster_url != 'None':
            x.poster_path = 'https://image.tmdb.org/t/p/original' + poster_url
        else:
            x.poster_path = 'https://www.scifi-movies.com/images/site/en/affiche_nondisponible.jpg'
        x.save()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'profile': profile, 'fav_movies': fav_movies}
    return render(request, 'MovieRecommender/profile.html', context)