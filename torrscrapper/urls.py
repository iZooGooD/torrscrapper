from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("searchTorrents",views.searchTorrents,name="searchTorrents"),
    path("dmca",views.dmca,name="dmca"),
    path("privacy_policy",views.privacy_policy,name="privacy_policy"),
    path("contact_us",views.contact_us,name="contact_us"),
    path("contact_us/submitform",views.contact_form_submit,name="contact_form_submit"),
    path("categories/movies",views.movies,name="movies"),
    path("categories/movies/<int:movie_id>",views.movies_single,name="movies_single"),
    path("categories/games",views.games,name="games"),
    path("categories/games/<int:game_id>",views.games_single,name="games_single"),
]
