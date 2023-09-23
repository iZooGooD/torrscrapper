from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.http import HttpResponse
from torrscrapper.models import Movies, Games, Contact
from django.core.paginator import Paginator
import requests
from bs4 import BeautifulSoup
import cloudscraper

# Constants for URLs
MAGNET_DL_BASE_URL = "https://magnetdl.unblockit.esq/"
X1337_BASE_URL = "https://1337x.unblockit.esq/"


# Create your views here.
def index(request):
    return render(request,"torrscrapper/index.html")

def searchTorrents(request):
    print("Search Method was called successfully")
    context={}

def searchTorrents(request):
    context = {}
    if 'keywords' in request.GET:
        keywords = request.GET['keywords'].lower()
        context['search_flag'] = True
        context['keywords'] = keywords

        extracted_links = []

        for i in range(1, 3):
            url = f"{MAGNET_DL_BASE_URL}{keywords[0]}/{keywords.replace(' ', '-')}/se/desc/{i}/"
            text = make_request(url)
            
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                extracted_links += extract_magnet_links(soup)

        on_1337x = True  # You can set this flag based on your logic

        if on_1337x:
            url = f"{X1337_BASE_URL}sort-search/{keywords}/seeders/desc/1/"
            text = make_request(url)
            
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                extracted_links += extract_magnet_links(soup)

        # Sorting the results by seeds in descending order
        results = sorted(extracted_links, key=lambda item: int(item['seeds']), reverse=True)
        context["torrents"] = results

        return render(request, "torrscrapper/searchResults.html", context)

    return redirect('index')

# Helper Function for Making Requests
def make_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return ""

# Helper Function for Extracting Magnet Links
def extract_magnet_links(soup):
    """
    Extract magnet links from a BeautifulSoup object containing HTML data.

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing HTML data.

    Returns:
        list: A list of dictionaries, each containing 'title' and 'magnet' keys.
    """
    extracted_links = []
    
    # Adjust this selector based on the structure of your HTML
    torrent_items = soup.find_all('div', class_='torrent-item')

    for item in torrent_items:
        title = item.find('div', class_='title').text.strip()
        magnet = item.find('a', class_='magnet-link')['href']
        
        extracted_links.append({'title': title, 'magnet': magnet})

    return extracted_links


# Helper Function for Validating Input Length
def validate_input_length(value, min_length, max_length):
    return min_length <= len(value) <= max_length

# Search Torrents View
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
            url = f"{MAGNET_DL_BASE_URL}{keyword[0]}/{keyword.replace(' ', '-')}/se/{order_by}/{i}/"
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
            url = f"{X1337_BASE_URL}sort-search/{keyword}/seeders/{order_by}/1/"
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
        entry = Contact.objects.create(name=name, email=email, subject=subject, message=message)
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
