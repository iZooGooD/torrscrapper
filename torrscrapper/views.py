from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages,auth
from django.http import HttpResponse
from torrscrapper.models import Movies,Games,Contact
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import requests
from bs4 import BeautifulSoup
import cloudscraper
from operator import itemgetter 

# Create your views here.
def index(request):
    return render(request,"torrscrapper/index.html")

def searchTorrents(request):
    print("Search Method was called successfully")
    context={}
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        context['search_flag']=True
        context['keywords']=keywords

        ##magnet dl
        keyword=keywords.lower()
        extracted_links=[] ## all data will be in this list
        page_title="working"
        order_by="desc"
        f_results2=[]
        on_1337x=True
        print("This message is just before trying to send request")
        for i in range(1,3):
            print("Right inside the for loop")
            url="https://magnetdl.unblockit.buzz/"+keyword[0]+"/"+keyword.replace(' ','-')+"/se/"+order_by+'/'+str(i)+"/"
            print("setting up url successfull")
            scraper = cloudscraper.create_scraper(browser='chrome') ## to prevent cloud fare auto bot page to detect bots
            print("Created the cloud scraper succesfully")
            print("Now making the request")
            try:
                text=scraper.get(url).text
                print("request was successfull")
            except Exception as e:
                print("There was an error "+str(e))
                
            soup=BeautifulSoup(text,'html.parser')
            print("Soup object success")
                
            # getting all titles
            titles=soup.findAll(class_="n")
            # torrents[0].contents[0]['title']
            
            # getting magnet
            magnets=soup.findAll(class_="m")
            # torrents[0].contents[0]['href']
            # getting seeds
            seeds=soup.findAll(class_="s")
            # print(torrents[0].string)
            # getting leeches
            peers=soup.findAll(class_="l")
            # print(torrents[0].string)
            ####### get the sizes
            sizes=[]
            torrents=soup.findAll("tr")
            for torrent in torrents:
                try:
                    if torrent.findChildren()[9].string=='Size':
                        pass
                    else:
                        sizes.append(torrent.findChildren()[9].string)
                except:
                    pass
            
            
            for title,link,seed,peer,size in zip(titles,magnets,seeds,peers,sizes):
                try:
                    extracted_links.append([title.contents[0]['title'],link.contents[0]['href'],seed.string,peer.string,size])
                except:
                    pass
            f_results1=[]
            for item in extracted_links:
                temp={'title':item[0],'magnet':item[1],'seeds':item[2],'peers':item[3],'size':item[4]}
                f_results1.append(temp)
        
        ###1337x
        if on_1337x:
            url="https://1337x.unblockit.buzz/sort-search/"+keyword+"/seeders/"+order_by+"/"+str("1")+"/"
            scraper = cloudscraper.create_scraper(browser='chrome') ## to prevent cloud fare auto bot page to detect bots
            text=scraper.get(url).text
            extracted_links2=[]
            soup=BeautifulSoup(text,'html.parser')
            torrents=soup.findAll(class_="name")
            find_seeds=soup.findAll(class_="seeds")
            find_leeches=soup.findAll(class_="leeches")
            find_sizes=soup.findAll(class_="size") 
            for (items,seeds,leeches,size) in zip(torrents,find_seeds,find_leeches,find_sizes):
                try:
                    href_link=items.contents[1].get("href")
                    magnet=""
                    href_link=href_link.replace("/","",1)
                    scraper = cloudscraper.create_scraper(browser='chrome')
                    url="https://1337x.unblockit.buzz/"+href_link
                    text=scraper.get(url).text
                    soup=BeautifulSoup(text,'html.parser')
                    for link in soup.find_all("a"):
                        if len(link.get("href"))>100:
                            magnet=link.get("href")
                            
                            
                            break
                    extracted_links2.append([items.contents[1].string,magnet,seeds.string,leeches.string,size.contents[0].string])
                except:
                    pass
                f_results2=[]
                for item in extracted_links2:
                    temp={'title':item[0],'magnet':item[1],'seeds':item[2],'peers':item[3],'size':item[4]}
                    f_results2.append(temp)

        results=f_results1+f_results2
        results2=sorted(results, key = lambda item: int(item['seeds']),reverse=True)
        context["torrents"]=results2
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
