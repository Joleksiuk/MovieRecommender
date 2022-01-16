from MovieRecommender.views import *


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
    i=0
    index = rand.randint(1, Movie.objects.all().count())
    while i < 12:

        try:
            movie = Movie.objects.get(id=index)
        except:
            movie = get_movie_from_API(index)
        i = i + 1
        if movie is not None:
            if movie.adults != 'True':
                movies.append(movie)

        index += 1

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages,'movies': movies}

    return render(request, 'MovieRecommender/home.html', context)
