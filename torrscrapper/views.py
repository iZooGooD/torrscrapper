from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.http import HttpResponse
from torrscrapper.models import Movies,Games,Contact
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

def privacy_policy(request):
    return render(request,"torrscrapper/privacy.html")

def contact_us(request):
    context={}
    context['submission']=False
    context['errors']=[]
    return render(request,"torrscrapper/contact.html",context)

def contact_form_submit(request):
    context={}
    errors=[]
    context['success']=False
    name=request.POST['name']
    email=request.POST['email']
    subject=request.POST['subject']
    message=request.POST['message']
    if len(name)>100 or len(name)<2:
        errors.append("Your name should be between 2 to 100 characters")
    if len(subject)>200 or len(subject)<4:
        errors.append("Your subject should be between 4 to 200 characters")
    if len(message)>500 or len(message)<10:
        errors.append("Message should be between 10 to 500 characters")

    if len(errors)==0:
        entry = Contact.objects.create(name=name,email=email,subject=subject,message=message)
        context['success']=True
        return render(request,"torrscrapper/contact.html",context)
    else:
        context['errors']=errors
        context['success']=False
        return render(request,"torrscrapper/contact.html",context)

    

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
    context['all_movies_length']=len(all_entries)
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
    context={}
    context['search_flag']=False
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        context['search_flag']=True
        context['search_keywords']=keywords
        all_entries = Games.objects.all().filter(title__contains=keywords)
        context['search_length']=len(all_entries)
        paginator=Paginator(all_entries,6)
        page=request.GET.get('page')
        paged_listing=paginator.get_page(page)
        context["all_games"]=paged_listing
        return render(request,"torrscrapper/category/games.html",context)

    all_entries = Games.objects.all()
    context['all_games_length']=len(all_entries)
    paginator=Paginator(all_entries,6)
    page=request.GET.get('page')
    paged_listing=paginator.get_page(page)
    context["all_games"]=paged_listing
    return render(request,"torrscrapper/category/games.html",context)

def games_single(request,game_id):
    game=get_object_or_404(Games,pk=game_id)
    context={'game':game}
    return render(request,"torrscrapper/category/games_single.html",context)
