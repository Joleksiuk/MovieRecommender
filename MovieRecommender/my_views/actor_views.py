from MovieRecommender.views import *


def actor_profile(request, pk):

    actor = get_actor_from_API(pk)
    movies = get_actor_movies_from_API(actor.actor_id)

    context = {'actor': actor, 'movies':movies}
    return render (request, 'MovieRecommender/actor.html', context)