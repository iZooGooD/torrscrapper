from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.http import HttpResponse
from torrscrapper.models import Movies
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from torrscrapper.searchtorrents import client_query

# Create your views here.
def index(request):
    return render(request,"torrscrapper/index.html")

def searchTorrents(request):
    context={}
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        context['search_flag']=True
        context['keywords']=keywords
        results=client_query(keywords)
        context["torrents"]=results
        return render(request,"torrscrapper/searchResults.html",context)
    return redirect('index')

def dmca(request):
    return render(request,"torrscrapper/DMCA.html")

def movies(request):
    context={}
    context['search_flag']=False
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        context['search_flag']=True
        context['search_keywords']=keywords
        all_entries = Movies.objects.all().filter(title__contains=keywords)
        context['search_length']=len(all_entries)
        paginator=Paginator(all_entries,15)
        page=request.GET.get('page')
        paged_listing=paginator.get_page(page)
        context["all_movies"]=paged_listing
        return render(request,"torrscrapper/category/movies.html",context)

    all_entries = Movies.objects.all()
    paginator=Paginator(all_entries,20)
    page=request.GET.get('page')
    paged_listing=paginator.get_page(page)
    context["all_movies"]=paged_listing
    return render(request,"torrscrapper/category/movies.html",context)

def movies_single(request,movie_id):
    movie=get_object_or_404(Movies,pk=movie_id)
    context={'movie':movie}
    return render(request,"torrscrapper/category/movies_single.html",context)

def games(request):
    return render(request,"torrscrapper/category/games.html")

def games_single(request):
    return render(request,"torrscrapper/category/games_single.html")