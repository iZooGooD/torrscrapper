# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:32:18 2020

@author: iZooGooD
"""
import requests
import sqlite3
from bs4 import BeautifulSoup
import cloudscraper



def extract_links_magnetdl(keyword,max_crawl_page=2,order_by='desc'):
    keyword=keyword.lower()
    page_number=1
    extracted_links=[] ## all data will be in this list
    page_title="working"
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    while page_title.find('Error'):
        
        if page_number>max_crawl_page:
            break
        url="https://magnetdl.unblockit.ltd/"+keyword[0]+"/"+keyword.replace(' ','-')+"/se/"+order_by+'/'+str(page_number)+"/"
        scraper = cloudscraper.create_scraper(browser='chrome') ## to prevent cloud fare auto bot page to detect bots
        text=scraper.get(url).text
        soup=BeautifulSoup(text,'html.parser')
        
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
        page_number+=1
    return extracted_links





## brute force to get all links at once
def extract_links_1337x(keyword,max_crawl_page=1,order_by='desc'):
    page_number=1
    extracted_links=[] ## all data will be in this list
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    page_title="working"
    while page_title.find('Error'):
        if page_number>max_crawl_page:
            break
        url="https://1337x.unblockit.ltd/sort-search/"+keyword+"/seeders/"+order_by+"/"+str(page_number)+"/"
        scraper = cloudscraper.create_scraper(browser='chrome') ## to prevent cloud fare auto bot page to detect bots
        text=scraper.get(url).text
        soup=BeautifulSoup(text,'html.parser')
        page_title=soup.title.string
        torrents=soup.findAll(class_="name")
        find_seeds=soup.findAll(class_="seeds")
        find_leeches=soup.findAll(class_="leeches")
        find_sizes=soup.findAll(class_="size") 
        for (items,seeds,leeches,size) in zip(torrents,find_seeds,find_leeches,find_sizes):
            try:
                magnet=generate_magnet_1337x(items.contents[1].get("href"))
                extracted_links.append([items.contents[1].string,magnet,seeds.string,leeches.string,size.contents[0].string])
            except:
                pass
        ##return a list in the order of title,href(link),seeds,leeches
        page_number+=1
    return extracted_links




##method will generate the magnet link you need to pass the href link from above method which is 2nd param
## only for 1337x
def generate_magnet_1337x(href_link):
    magnet=""
    href_link=href_link.replace("/","",1)
    scraper = cloudscraper.create_scraper(browser='chrome')
    url="https://1337x.unblockit.ltd/"+href_link
    text=scraper.get(url).text
    soup=BeautifulSoup(text,'html.parser')
    for link in soup.find_all("a"):
        if len(link.get("href"))>100:
            magnet=link.get("href")
            break
    return magnet
            
       


def client_query(keywords):
    results=[]
    f_results=[]
    try:
        results_1337x=extract_links_1337x(keywords)
        results_magnetdl=extract_links_magnetdl(keywords)
        results=results_1337x+results_magnetdl
        for item in results:
            temp={'title':item[0],'magnet':item[1],'seeds':item[2],'peers':item[3],'size':item[4]}
            f_results.append(temp)
        
        
        
    except:
        results.append("Error")
    return f_results
    







    




    
    
 
