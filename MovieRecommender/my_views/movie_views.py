from MovieRecommender.views import *


def addToFavourites(request, pk):

    movie = Movie.objects.get(movie_id=pk)
    user = request.user
    profile = Profile.objects.get(user_id=user)
    profile.fav_movies.add(movie)
    return redirect('movie', movie.id)


def movie(request, pk):

    movie = Movie.objects.get(id=pk)
    poster_url = get_poster_url(movie.movie_id)
    result = 'https://image.tmdb.org/t/p/original' + poster_url
    movie.poster_path=result

    genres_dic = get_api_value(movie.movie_id, 'genres')
    genres =[]
    for x in range(0, len(genres_dic)):
        genres.append(genres_dic[x]['name'])

    companies_dic = get_api_value(movie.movie_id, 'production_companies')
    companies=[]
    for x in range(0, len(companies_dic)):
        companies.append(companies_dic[x]['name'])

    try: rating = Rating.objects.get(movie = movie,user = request.user)
    except: rating = 'Not rated'

    context={'movie': movie, 'genres': genres, 'companies': companies, 'rating':rating}
    return render(request,"MovieRecommender/movie.html", context)


@csrf_exempt
def rate_movie(request):
    data = json.loads(request.body)
    movie_id = data['movie_id']
    try:
        movie = Movie.objects.get(id=movie_id)
    except:
        movie = None

    rating_value = data['value']
    user = request.user
    print(data)
    print('Movie: ', movie, " User: ", user, ' Rating: ', rating_value)

    try:
        rating = Rating.objects.get(user= user,movie=movie)
    except:
        rating = None

    if rating is not None:
        print('Updated')
        rating.value=rating_value
        rating.save()
    else:
        print('Created')
        Rating.objects.create(
            movie=movie,
            value=rating_value,
            user=user
        )

    response = HttpResponse(request)
    response.status_code = 200
    return response
