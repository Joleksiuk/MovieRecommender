from MovieRecommender.views import *


@login_required(login_url='login')
def collab_filter(request):

    movies = list(recommend_movies_by_collaborative_filtering(request))[0:50]
    context = {"movies": movies}

    return render(request, 'MovieRecommender/collab_filtering.html', context)


def similiar_ratings_user(request):
    # similar ratings to movies
    common_ratings_users = []
    user_id = request.user.id

    ratings = Rating.objects.filter(user_id=user_id).values()
    for i in range(0, ratings.count()):
        sql = 'SELECT * From auth_user as u ' \
              'JOIN (SELECT mr.user_id from MovieRecommender_rating  as mr ' \
              'JOIN (SELECT * from MovieRecommender_rating ' \
              'WHERE movie_id = ' + str(ratings[i]['movie_id']) + ') as t ' \
                                                                  'ON t.id = mr.id AND (abs(mr.value - t.value) <= 1 AND t.user_id != ' + str(
            user_id) + ')) as t2 ' \
                       'ON u.id = t2.user_id'
        for x in User.objects.raw(sql):
            common_ratings_users.append(x.id)

    result_list = count_frequencies(common_ratings_users)
    df = p.DataFrame(columns=['user_id', 'count'])
    for x in result_list:
        df = df.append(x, ignore_index=True)

    return df.head(10)


def familiar_favourite_movies_users(request):
    # most similiar favourites
    my_user = request.user
    fav_movies = Profile.objects.filter(user_id=my_user).values_list('fav_movies', flat=True)

    columns = ['user_id', 'count']
    df = p.DataFrame(columns=columns)

    for x in range(8, User.objects.all().count()):

        element = {}
        other_fav_movies = Profile.objects.filter(user_id=User.objects.get(id=x)).values_list('fav_movies',
                                                                                              flat=True)
        element['user_id'] = x
        element['count'] = fav_movies.intersection(other_fav_movies).count()
        df = df.append(element, ignore_index=True)

    df = df.sort_values(by=['count'], axis=0, ascending=False, inplace=False, kind='quicksort')
    return df.head(100).tail(99)


def sum_similarity_points(similar_ratings_df, df):

    for date, row in similar_ratings_df.T.iteritems():

        if row['user_id'] in df['user_id'].values:
            points = row['count'] + df.loc[df['user_id'] == row['user_id'], 'count'].to_numpy()
            df.loc[df['user_id'] == row['user_id'], 'count'] = points
        else:
            df = df.append(row.to_dict(), ignore_index=True)

    df = df.sort_values(by=['count'], axis=0, ascending=False, inplace=False, kind='quicksort')
    return df.head(10)['user_id'].values


def recommend_movies_by_collaborative_filtering(request):
    similar_ratings_df = similiar_ratings_user(request)
    familiar_favourites_df = familiar_favourite_movies_users(request)

    users_list = sum_similarity_points(similar_ratings_df, familiar_favourites_df)
    x = get_top_rated_user_movies(15, request.user.id)

    movies_num = 20
    final_movie_list = []
    for x in range(0, len(users_list)):
        y = get_top_rated_user_movies(movies_num, users_list[x])
        final_movie_list = [*final_movie_list, *y]
        if movies_num > 5:
            movies_num -= 1

    return set(final_movie_list)
