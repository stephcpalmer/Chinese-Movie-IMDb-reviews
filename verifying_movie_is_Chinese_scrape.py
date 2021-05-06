from reppy.robots import Robots
import urllib.request, re
from bs4 import BeautifulSoup
import pandas as pd

#first check to see if ok to scrape user ratings data   ##From reppy github documentation ##tt0013807
Url = 'https://www.imdb.com/title/tt*/'
robots = Robots.fetch('https://www.imdb.com/robots.txt')

Base_url = 'https://www.imdb.com/title/'   

User_review_dict = {}
if robots.allowed(Url, 'SCP') is False: #Making sure that I am allowed to scrape from the movie title's page   #I can so this won't happen, but just in case
    print(f"Cannot scrape from {Url}.")   

else:
    delay = robots.agent('SCP').delay   #Checking to see if there is a crawl delay specified   #There is none 
    Col_names = ['Id','Primary Title','Original Title','Year','Genres','Average Rating','# of Votes']
    data = pd.read_csv('Chinese_movies.txt', delimiter = ",",header=0,names=Col_names,error_bad_lines=False) #Creating database from Mandarin movie file #some movies don't have reviews->bad, not keeping those for analysis

    print('check')
    for i in range(len(data.index)):
        with urllib.request.urlopen(Base_url+data.at[i,'Id']) as request:
            soup = BeautifulSoup(request.read(),'lxml')
        try:
            Country_of_origin = soup.find('h4',string='Country:').parent.contents[3].text
            if Country_of_origin != 'China':
                data = data.drop(i)
        except AttributeError:
            data.drop(i)
        print(i)

    data.to_csv('DataFrame.txt')


    






