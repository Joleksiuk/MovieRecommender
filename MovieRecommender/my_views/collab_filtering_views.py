from MovieRecommender.views import *


def collab_filter(request):
    context = {}
    return render(request, 'MovieRecommender/collab_filtering.html', context )