from MovieRecommender.views import *


def collab_filter(request):
    context = {}
    return render(request, 'MovieRecommender/collab_filtering.html', context)


def similiar_ratings_user(request):
    # similar ratings to movies
    common_ratings_users = []
    user_id= request.user.id

    ratings = Rating.objects.filter(user_id=user_id).values()
    for i in range(0, ratings.count()):
        sql = 'SELECT * From auth_user as u ' \
              'JOIN (SELECT mr.user_id from MovieRecommender_rating  as mr ' \
                    'JOIN (SELECT * from MovieRecommender_rating ' \
                    'WHERE movie_id = '+ str(ratings[i]['movie_id']) +') as t ' \
                    'ON t.id = mr.id AND (abs(mr.value - t.value) <= 1 AND t.user_id != '+str(user_id)+')) as t2 ' \
                'ON u.id = t2.user_id'
        for x in User.objects.raw(sql):
            common_ratings_users.append(x.id)

    print(common_ratings_users)
    my_dict = {i:common_ratings_users.count(i) for i in common_ratings_users}
    print(my_dict)
    df = p.DataFrame(columns=['user_id', 'count'])
    df = df.append(my_dict,ignore_index=True)
    print(df)


def familiar_favourite_movies_users(request):
    # most similiar favourites
    my_user = request.user
    fav_movies = Profile.objects.filter(user_id=my_user).values_list('fav_movies', flat=True)

    columns = ['user_id', 'common_fav_movie_count']
    df = p.DataFrame(columns=columns)

    for x in range(1, User.objects.all().count()):
        try:
            element = {}
            other_fav_movies = Profile.objects.filter(user_id=User.objects.get(id=x)).values_list('fav_movies',
                                                                                                  flat=True)
            element['user_id'] = x
            element['common_fav_movie_count'] = fav_movies.intersection(other_fav_movies).count()
            df = df.append(element, ignore_index=True)
        except:
            print('Error: There is no user with id ', x)

    df = df.sort_values(by=['common_fav_movie_count'], axis=0, ascending=False, inplace=False, kind='quicksort')
    common_favourite_movies = df.head(10)['user_id'].values
    return common_favourite_movies
