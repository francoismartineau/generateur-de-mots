from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #DEAD path('random-words', views.random_words, name='random_words'),
    path('random-syllables-words', views.random_syllables_words, name='random_syllables_words'),
    path('random-with-criterias', views.random_with_criterias, name='random_with_criterias'),
    path('wikipedia-random-words', views.wikipedia_random_words, name='wikipedia_random_words'),
]