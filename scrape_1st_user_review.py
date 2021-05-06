from reppy.robots import Robots
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pprint

#first check to see if ok to scrape user ratings data   ##From reppy github documentation ##tt0013807
Url = 'https://www.imdb.com/title/tt*/reviews'
robots = Robots.fetch('https://www.imdb.com/robots.txt')

Base_url = 'https://www.imdb.com/title/'
End_url = '/reviews/'
User_reviews_dict = {}
if robots.allowed(Url, 'SCP') is False: #Making sure that I am allowed to scrape from the movie title's page   #I can so this won't happen, but just in case
    print(f"Cannot scrape from {Url}.")   

else:
    delay = robots.agent('SCP').delay   #Checking to see if there is a crawl delay specified   #There is none 
    data = pd.read_csv('DataFrame.txt', delimiter = ",")
    data = data.drop(columns = 'Unnamed: 0')

    for i in range(len(data.index)):
        try:
            with urllib.request.urlopen(Base_url+data.at[i,'Id']+End_url,timeout=10) as request:
                    soup = BeautifulSoup(request.read(),'lxml')
            try:
                User_reviews = soup.find("div", {"class": "text show-more__control"})   # a list of user reviews #limited to 5 # call User_reviews[i].contents for individual reviews
                User_reviews_dict[data.at[i,'Id']] = User_reviews.text
            except:
                data.drop(i)
        except: 
            print(f"Request for {i}'s user reviews timed out")

        print(i)
    
with open('User_reviews.txt', 'w',encoding='utf8') as wf:
    wf.write(pprint.pformat(User_reviews_dict, depth=1))




    






