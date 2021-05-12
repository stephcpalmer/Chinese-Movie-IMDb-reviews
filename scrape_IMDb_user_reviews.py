import urllib.request, pprint, re
from bs4 import BeautifulSoup
import pandas as pd

Base_url = 'https://www.imdb.com/title/'
End_url = '/reviews/'

data = pd.read_csv('Textfiles/Dataframe.txt', delimiter = ",")
data = data.drop(columns = 'Unnamed: 0')
    
User_reviews_dict = {}
User_ratings_df = pd.DataFrame()

for i in range(len(data.index)):
    try:
        with urllib.request.urlopen(Base_url+data.at[i,'Id']+End_url,timeout=10) as request:
                soup = BeautifulSoup(request.read(),'lxml')
        try:
            User_reviews = soup.find_all('div', {'class': 'text show-more__control'})   # a list of user reviews # removed limit in hopes to improve topic models # call User_reviews[i].contents for individual reviews
            User_reviews_dict[data.at[i,'Id']] = {} #creating nested dictionary {'id1':{0:'first review',1:'second review},'id2':{0:'first review of 2nd id',1:'second review of 2nd id}}...
            
            Ratings = []
            for j in range(len(User_reviews)):
                User_reviews_dict[data.at[i,'Id']][j] = User_reviews[j].text
                
            for k in range(len(User_reviews)):
                user_rating_num = data.at[i,'Id']+'_'+str(k)
                
                if len(User_reviews[k].parent.parent.contents)== 7: # no rating
                    rating = 'N/A'
                    user = User_reviews[k].parent.parent.contents[3].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[3].contents[2].text
                
                    
                if len(User_reviews[k].parent.parent.contents) == 11: # no rating & spoiler
                    rating = 'N/A'
                    user = User_reviews[k].parent.parent.contents[3].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[3].contents[2].text

                    
                if len(User_reviews[k].parent.parent.contents) == 13: # spoiler
                    rating = re.sub('\n','',User_reviews[k].parent.parent.contents[1].text)
                    user = User_reviews[k].parent.parent.contents[5].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[5].contents[2].text

                    
                if len(User_reviews[k].parent.parent.contents) == 9: # regular
                    rating = re.sub('\n','',User_reviews[k].parent.parent.contents[1].text)
                    user = User_reviews[k].parent.parent.contents[5].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[5].contents[2].text
                
                Ratings.append([user_rating_num,user,rating,date_posted])
                
            User_ratings_df = User_ratings_df.append(Ratings,ignore_index=True)
                
        except:
            data.drop(i)
        print(i)
    except: 
        print(f"Request for {i}'s user reviews timed out")
 
with open('Textfiles/User_reviews.txt', 'w',encoding='utf8') as wf:
    wf.write(pprint.pformat(User_reviews_dict, depth=2))        
 
User_ratings_df = User_ratings_df.rename(columns={0:'Id',1:'User',2:'Rating',3:'Date Posted'})
User_ratings_df.to_csv('Textfiles/User_ratings_dataframe.txt')


 