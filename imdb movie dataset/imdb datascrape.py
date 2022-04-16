## Load libraries
from logging.handlers import RotatingFileHandler
import requests 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs 

counter = 0;
#variable to store data
movie_name = [] 
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
genre = []
country = []
company = []



def scrapepage(page,url):
    response = requests.get(url)
    soup =  bs(response.content,'html.parser')
    movie_data = soup.find_all('div',attrs = {'class': 'lister-item mode-advanced'})
    for storing in movie_data:
        
        name = storing.h3.a.text
        #global counter
        #print(counter+' '+ name)
        #counter = counter + 1
        
        movie_name.append(name)
        
        #return movie year released
        year_released = storing.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
        year.append(year_released)
        
        #return movie duration
        duration = storing.p.find('span', class_ ='runtime').text.replace(' min','')
        time.append(duration)
        
        #return movie user rating
        rate = storing.find('div', class_ ='inline-block ratings-imdb-rating').text.replace('\n', '')
        rating.append(rate)
        
        #return movie metascore
        meta = storing.find('span', class_ = 'metascore').text.replace(' ','') if storing.find('span', class_ = 'metascore') else '-'
        metascore.append(meta)
        
        nv_values = storing.find_all('span', attrs = {'name': 'nv'})
        
        #return movie votes
        vote = nv_values[0].text
        votes.append(vote)
        
        #return movie total gross
        grosses = nv_values[1].text if len(nv_values) > 1 else '-' 
        gross.append(grosses)
        
        #return movie genre
        genres = storing.p.find('span', class_ = 'genre').text.replace('\n','')
        genre.append(genres)
        
        titleid = storing.find('h3', class_ ='lister-item-header').a.get('href')
        detaillink = 'https://www.imdb.com'+titleid+'?ref_=adv_li_tt'
        
        detailres = requests.get(detaillink)
        detailsoup = bs(detailres.content,'html.parser')
        movie_details = detailsoup.find('div',attrs = {'data-testid': 'title-details-section'}).ul
        
        origin = movie_details.find('li',attrs = {'data-testid': 'title-details-origin'}).div.ul
        origins = origin.findChildren("a")
        location = ''
        for child in origins:
            location = location +'/'+ child.text
        country.append(location)

      
        origin = movie_details.find('li',attrs = {'data-testid': 'title-details-companies'}).div.ul
        origins = origin.findChildren("a")
        companies = ''
        for child in origins:
            companies = companies +'/'+ child.text
            
        company.append(companies)
        
        
    

count = 1
while count < 1000:
    #print(count)
    pastecount = str(count)
    url ='https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=200&start='+pastecount+'&ref_=adv_nxt'
    print(url)
    scrapepage(count,url)
    #countadd(count)
    
    count+=200

movie_df = pd.DataFrame({'Name of movie':movie_name ,'Year of release':year, 'Duration':time ,'Movie Rating':rating , 'Metascore':metascore ,'Votes':votes,'Gross Collection':gross, 'Genres':genre})

#movie_df = pd.DataFrame({'Name of movie':movie_name ,  'Year of release': year ,'Countries of origin': origin, 'Duration': time ,'Movie Rating': rating 
#                            , 'Metascore': metascore ,'Votes': votes,'Gross Collection':gross, 'Genres':genre, 'Production companies':production_company})
    
print(movie_df)
movie_df.to_csv('movie-dataset-fully-scraped.csv',index=False)




