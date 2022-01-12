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

    test = Movie.objects.filter(genres__name='Comedy')

    i=0
    index = rand.randint(1, Movie.objects.all().count())
    while i <12:

        movie = Movie.objects.get(id=index)
        poster_url = get_poster_url(movie.movie_id)

        if poster_url is not None:

            result = 'https://image.tmdb.org/t/p/original' + str(poster_url)
            movie.poster_path = result
            i=i+1
            movies.append(movie)
        index+=1


    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages,'movies': movies, "test": test}

    return render(request, 'MovieRecommender/home.html', context)
