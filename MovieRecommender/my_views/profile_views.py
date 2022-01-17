from MovieRecommender.views import *

@login_required(login_url='login')
def userProfile(request, pk):
    try:
        user = User.objects.get(id=pk)
    except:
        print('User does not exist')

    profile = Profile.objects.get(user_id=user)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    fav_movies = profile.fav_movies.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'profile': profile, 'fav_movies': fav_movies}
    return render(request, 'MovieRecommender/profile.html', context)