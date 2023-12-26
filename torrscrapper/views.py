from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.http import HttpResponse
from torrscrapper.models import Movies, Games, Contact
from django.core.paginator import Paginator
from .scraping_utils import scrape_data

def index(request):
    return render(request,"torrscrapper/index.html")

# Helper Function for Validating Input Length
def validate_input_length(value, min_length, max_length):
    return min_length <= len(value) <= max_length

# Search Torrents View
def searchTorrents(request):
    context={}
    keywords = request.GET['keywords'].lower()
    torrents_data = scrape_data(keywords)
    context["torrents"]= torrents_data
    context["keywords"] = keywords
    return render(request,"torrscrapper/searchResults.html",context)

# DMCA View
def dmca(request):
    return render(request, "torrscrapper/DMCA.html")

# Privacy Policy View
def privacy_policy(request):
    return render(request, "torrscrapper/privacy.html")

# Contact Us View
def contact_us(request):
    context = {'submission': False, 'errors': []}
    return render(request, "torrscrapper/contact.html", context)

# Contact Form Submission View
def contact_form_submit(request):
    context = {'success': False, 'errors': []}
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')

    if not validate_input_length(name, 2, 100):
        context['errors'].append("Your name should be between 2 to 100 characters")

    if not validate_input_length(subject, 4, 200):
        context['errors'].append("Your subject should be between 4 to 200 characters")

    if not validate_input_length(message, 10, 500):
        context['errors'].append("Message should be between 10 to 500 characters")

    if not context['errors']:
        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        context['success'] = True

    return render(request, "torrscrapper/contact.html", context)

# Movies View
def movies(request):
    context = {'search_flag': False}
    keywords = request.GET.get('keywords', '')

    if keywords:
        context['search_flag'] = True
        context['search_keywords'] = keywords

        all_entries = Movies.objects.filter(title__icontains=keywords)
        context['search_length'] = len(all_entries)

        paginator = Paginator(all_entries, 15)
        page = request.GET.get('page')
        paged_listing = paginator.get_page(page)
        context["all_movies"] = paged_listing
    else:
        all_entries = Movies.objects.all()
        context['all_movies_length'] = len(all_entries)

        paginator = Paginator(all_entries, 20)
        page = request.GET.get('page')
        paged_listing = paginator.get_page(page)
        context["all_movies"] = paged_listing

    return render(request, "torrscrapper/category/movies.html", context)

# Single Movie View
def movies_single(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    context = {'movie': movie}
    return render(request, "torrscrapper/category/movies_single.html", context)

# Games View
def games(request):
    context = {'search_flag': False}
    keywords = request.GET.get('keywords', '')

    if keywords:
        context['search_flag'] = True
        context['search_keywords'] = keywords

        all_entries = Games.objects.filter(title__icontains=keywords)
        context['search_length'] = len(all_entries)

        paginator = Paginator(all_entries, 6)
        page = request.GET.get('page')
        paged_listing = paginator.get_page(page)
        context["all_games"] = paged_listing
    else:
        all_entries = Games.objects.all()
        context['all_games_length'] = len(all_entries)

        paginator = Paginator(all_entries, 6)
        page = request.GET.get('page')
        paged_listing = paginator.get_page(page)
        context["all_games"] = paged_listing

    return render(request, "torrscrapper/category/games.html", context)

# Single Game View
def games_single(request, game_id):
    game = get_object_or_404(Games, pk=game_id)
    context = {'game': game}
    return render(request, "torrscrapper/category/games_single.html", context)
