from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("searchTorrents",views.searchTorrents,name="searchTorrents"),
    path("dmca",views.dmca,name="dmca"),
    path("categories/movies",views.movies,name="movies"),
    path("categories/movies/<int:movie_id>",views.movies_single,name="movies_single"),
    path("categories/games",views.games,name="games"),
    path("categories/games/game",views.games_single,name="games_single"),
]
