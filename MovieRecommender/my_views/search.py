from MovieRecommender.views import *


def search(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    profiles = Profile.objects.filter(
        Q(name__contains=q)
    )

    print(profiles.values())

    search_value = q.replace(' ', '+')
    api_path = 'http://api.themoviedb.org/3/search/person?api_key=4b5f9777a2d363363cbb7d26017f0052&query=' +search_value
    response_API = requests.get(api_path)
    api_text = response_API.text
    data = json.loads(api_text)
    actors = []

    movies=Movie.objects.filter(
        Q(title__contains=q),
        Q(overview__contains=q)
    )

    for x in range(0, len(data['results'])):
        actor = get_actor_from_API(data['results'][x]['id'])
        actors.append(actor)

    print(actors)
    context = {'movies': movies, 'rooms': rooms, 'profiles': profiles, 'actors': actors}
    return render(request, 'MovieRecommender/search.html', context)
