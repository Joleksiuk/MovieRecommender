from MovieRecommender.views import *


def get_trailer_link(movie_id):
    base_url = "https://www.youtube.com/embed/"
    api_path = "https://api.themoviedb.org/3/movie/" + str(
        movie_id) + "/videos?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US"
    response_API = requests.get(api_path)
    data = response_API.text
    parse_json = json.loads(data)

    try:
        video_code = parse_json['results'][0]['key']
    except:
        video_code = 'None'

    if video_code != 'None':
        path = base_url + video_code
        return path
    else:
        return video_code


def addToFavourites(request, pk):
    movie = Movie.objects.get(movie_id=pk)
    user = request.user
    profile = Profile.objects.get(user_id=user)
    profile.fav_movies.add(movie)
    return redirect('movie', movie.id)




def get_similar_movies(request, pk):
    api_path = 'https://api.themoviedb.org/3/movie/'+str(pk)+'/similar?api_key=4b5f9777a2d363363cbb7d26017f0052&language=en-US&page=1'
    response_API = requests.get(api_path)
    api_text = response_API.text
    data = json.loads(api_text)

    movies = []
    for x in range(0, len(data['results'])):
        movie = get_movie_from_API(data['results'][x]['id'])
        movies.append(movie)

    movie = Movie.objects.filter(movie_id=pk).values()[0]

    context={'movies':movies, 'movie':movie}
    return render(request, "MovieRecommender/similar_movies.html", context)


def movie(request, pk):

    try:
        movie = Movie.objects.get(id = pk)
    except:
        movie = get_movie_from_API(pk)

    if movie is not None:
        genres=[]
        genres_obj = movie.genres.values()
        for x in range(0, len(genres_obj)):
            genres.append(genres_obj[x])

        #companies = movie.production_companies.values()
        try:
            user_rating = Rating.objects.get(movie=movie, user=request.user)
        except:
            user_rating = 'Not rated'

        trailer = get_trailer_link(movie.movie_id)

        cast = get_cast_from_API(movie.movie_id)
        print(cast)

        context = {'movie': movie,'user_rating': user_rating, 'trailer': trailer, 'actors': cast}
        return render(request, "MovieRecommender/movie.html", context)
    else:
        return redirect('home')




@csrf_exempt
def rate_movie(request):
    data = json.loads(request.body)
    movie_id = data['movie_id']
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        movie = Movie.objects.create(get_movie_from_API(movie_id))
        movie.save()

    new_rating = data['value']
    user = request.user
    print(data)
    print('Movie: ', movie, " User: ", user, ' Rating: ', new_rating)

    try:
        rating = Rating.objects.get(user=user, movie=movie)
    except:
        rating = None

    # Updating Rating
    if rating is not None:
        print('Updated')
        print('Before removing update: ',movie.vote_average, movie.vote_count)
        # Removing old rating from average rating
        if movie.vote_count != 1:
            movie.vote_average = ((movie.vote_average * movie.vote_count) - rating.value) / (movie.vote_count - 1)
            movie.vote_count = movie.vote_count-1
        else:
            movie.vote_average = 0.0
        movie.save()
        print('After removing update: ',movie.vote_average, movie.vote_count)

        rating.value = new_rating
        rating.save()
    # Creating new Rating
    else:
        print('Created')
        Rating.objects.create(
            movie=movie,
            value=new_rating,
            user=user
        )
    # Adding new rating to average rating
    new_movie_rating = (movie.vote_average + new_rating) / (movie.vote_count + 1)
    movie.vote_average = round(new_movie_rating,1)
    movie.vote_count = movie.vote_count + 1
    movie.save()
    print('After adding new rating: ', movie.vote_count," ", movie.vote_average," ")

    response = HttpResponse(request)
    response.status_code = 200
    return response
