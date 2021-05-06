from reppy.robots import Robots
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pprint, re

#first check to see if ok to scrape user ratings data   ##From reppy github documentation ##tt0013807
Url = 'https://www.imdb.com/title/tt*/reviews'
robots = Robots.fetch('https://www.imdb.com/robots.txt')

Base_url = 'https://www.imdb.com/title/'
End_url = '/reviews/'


if robots.allowed(Url, 'SCP') is False: #Making sure that I am allowed to scrape from the movie title's page   #I can so this won't happen, but just in case
    print(f"Cannot scrape from {Url}.")   

else:
    delay = robots.agent('SCP').delay   #Checking to see if there is a crawl delay specified   #There is none 
    data = pd.read_csv('Dataframe.txt', delimiter = ",")
    data = data.drop(columns = 'Unnamed: 0')
    
    User_reviews_dict = {}

    Col_names = ['Id','User','Rating','Date Posted']
    User_ratings_df = pd.DataFrame(columns=Col_names)
    
    
    for i in range(10):#len(data.index)
        try:
            with urllib.request.urlopen(Base_url+data.at[i,'Id']+End_url,timeout=10) as request:
                    soup = BeautifulSoup(request.read(),'lxml')
            try:
                User_reviews = soup.find_all('div', {'class': 'text show-more__control'})   # a list of user reviews # removed limit in hopes to improve topic models # call User_reviews[i].contents for individual reviews
                User_reviews_dict[data.at[i,'Id']] = {} #creating nested dictionary {'id1':{0:'first review',1:'second review},'id2':{0:'first review of 2nd id',1:'second review of 2nd id}}...
                for j in range(1,1+len(User_reviews)):
                    User_reviews_dict[data.at[i,'Id']][j] = User_reviews[j].text

                    User_ratings = soup.find_all('div',{'class':'ipl-ratings-bar'})
                    User_names_and_dates = soup.find_all('div',{'class':'display-name-date'})
                    for k in range(1,1+len(User_ratings)):
                        User_rating_num = data.at[i,'Id']+'_'+str(k)
                        User_ratings_df.at[i+j+k,'Id'] = User_rating_num
                            
                        User = User_names_and_dates[k].contents[1].text
                        User_ratings_df.at[i+j+k,'User'] = User
                            
                        Rating = re.sub('\n','',User_ratings[k].text)
                        User_ratings_df.at[i+j+k,'Rating'] = Rating
                            
                        Date_posted = User_names_and_dates[k].contents[2].text
                        User_ratings_df.at[i+j+k,'Date Posted'] = Date_posted
            except:
                data.drop(i)
        except: 
            print(f"Request for {i}'s user reviews timed out")

        print(i)
User_ratings_df.to_csv('User_ratings_dataframe.txt')
with open('User_reviews.txt', 'w',encoding='utf8') as wf:
    wf.write(pprint.pformat(User_reviews_dict, depth=2))

    






