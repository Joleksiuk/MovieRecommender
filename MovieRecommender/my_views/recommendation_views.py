from MovieRecommender.views import *


def rating_recommendation(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    ordering_dic = {'worst-rated': 'ORDER BY vote_average ASC, vote_count DESC',
                    'wbest-rated': 'ORDER BY vote_average DESC, vote_count DESC',
                    'most-ratings': 'ORDER BY vote_count DESC',
                    'least-ratings': 'ORDER BY vote_count ASC'}

    arg_list = q.split("%")
    genre = arg_list[0]
    order = ""
    order_sql = ""

    if len(arg_list) == 2:
        if arg_list[1] != "":
            order = arg_list[1]
            order_sql = ordering_dic[order]

    if genre!='all':
        sql = "SELECT m.id FROM MovieRecommender_movie as m " \
              "JOIN MovieRecommender_movie_genres as mg ON m.id = mg.movie_id " \
              "JOIN MovieRecommender_genre as g ON mg.genre_id = g.id " \
              "WHERE g.name = '" + str(genre) + "' " + order_sql + " LIMIT 20 "

    if genre == "":
        sql = "SELECT m.id FROM MovieRecommender_movie as m "+ order_sql + " LIMIT 5 "

    movies = []

    for m in Movie.objects.raw(sql):
        movie = m
        movies.append(movie)

    genres = Genre.objects.all()
    context = {'genres': genres, 'movies': movies, 'genre': genre, 'order': order}

    return render(request, 'MovieRecommender/rating_recommend.html', context)

