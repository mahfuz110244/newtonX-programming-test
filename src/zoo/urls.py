from django.urls import path

from .views import AnimalPopulationView, AnimalView, HungryAnimalsView, FeedAnimalView

app_name = 'zoo'

urlpatterns = [
    path('animal/', AnimalView.as_view(), name='animal-list'),
    path('animal/total-animal/', AnimalPopulationView.as_view(), name='animal-count-total'),
    path('animal/hungry-animal/', HungryAnimalsView.as_view(), name='animal-count-hungry'),
    path('animal/feed-update/', FeedAnimalView.as_view(), name='animal-feed-time'),
]
