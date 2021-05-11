import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

#first check to see if ok to scrape user ratings data

Base_url = 'https://www.imdb.com/title/'   
Col_names = ['Id','Primary Title','Original Title','Year','Genres','Average Rating','# of Votes']
data = pd.read_csv('Textfiles/Chinese_movies.txt', delimiter = ",",header=0,names=Col_names,error_bad_lines=False) #Creating database from Mandarin movie file #some movies don't have reviews->bad, not keeping those for analysis

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

data.to_csv('Textfiles/DataFrame.txt')


    






