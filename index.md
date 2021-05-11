## Objective
In this project I aim to analyze user reviews of Chinese movies from the IMDb website and draw some inferences about the western audience's perception of Chinese cinema.

## Motivation
This project is the final project of Professor Vierthaler's Spring 2021 CHIN 303 "Hacking Chinese Studies" class at William & Mary. From the time I was in high school, I have been beguiled by Chinese tv shows and movies. This interest in Chinese programs lead to me taking over 20 Chinese Studies credits at William & Mary even though most of them did not satisfy any of my liberal arts requirements. Thankfully, in my last semester at the College, I have found a class that intersects my academic focus in Applied Mathematics and my interest in Chinese language and culture. Hence, in the final project I wished to analyze Chinese movies, and since I am aware of IMDb's available datasets, and in my previous programming classes I have not learned how to web scrape, my ideas manifested as sourcing my analysis of Chinese movie user reviews from IMDb.

## Data Gathering and Cleaning
I pulled data from IMDb's datasets and scraping their title and user review pages for specific movies.

### Downloading and Unzipping IMDb Datasets

IMDb has subsets of their data [available](https://www.imdb.com/interfaces/) for personal and non-commercial use. Firstly, I downloaded the data from three of their datasets: title.akas, title.basics, and title.ratings by using the urllib package for Python.

```python
# code from download_and_unzip_IMDb_files.py
import urllib.request

Title_akas_request = urllib.request.urlretrieve(
                    'https://datasets.imdbws.com/title.akas.tsv.gz',
                    'Title_akas.tsv.gz')
Title_basics_request = urllib.request.urlretrieve(
                    'https://datasets.imdbws.com/title.basics.tsv.gz',
                    'Title_basics.tsv.gz')
Title_ratings_request = urllib.request.urlretrieve(
                    'https://datasets.imdbws.com/title.ratings.tsv.gz',
                    'Title_ratings.tsv.gz')

```
After downloading the desired zipped dataset files, I then had to unzip them. As they are gzip files, I used the python library gzip to unzip them, and I then saved the decompressed data as text files to my computer.
```python
# resulting txt files not in my GitHub repository as they are too large,
# running this code on your system will allow you to collect that data if desired
import gzip

with gzip.open('Textfiles/Title_akas.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_akas.txt','wb') as w:
        w.writelines(myzip)

with gzip.open('Textfiles/Title_basics.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_basics.txt','wb') as w:
        w.writelines(myzip)

with gzip.open('Textfiles/Title_ratings.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_ratings.txt','wb') as w:
        w.writelines(myzip)
```
Now that I have gathered all of the data in these IMDb datasets, I must filter the data about IMDb's $10 million + titles down to only their Chinese movies data.

### Cleaning IMDb Dataset Data
To leave only the data of movies from China, I created regular expressions using the re library to capture the title ids of titles in that have their region listed as China. This is the only data I captured from Title_akas, as it is the biggest dataset, and the other data I want to collect can be found in the other two smaller datasets. Turning to other basic data, I created a regex to capture the primary title, the original title, the start year, and genres of titles listed as movies. Finally, I created a regex to capture the average rating and the number of votes of a title.
```python 
# code from gather_IMDb_database_data.py
import re

#Title_akas header #titleId	ordering	title	region	language	types	attributes	isOriginalTitle
Chinese_titles_id_regex = re.compile(r'(tt\d{7}).+\tCN\t',re.X) #captures id if the title is from China
Id_regex = re.compile(r'(tt\d{7})')

#Title_basics header #tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres  ###Header from Title_basics.txt
Basics_info_regex = re.compile(r'tt\d{7}\tmovie\t([^\t]+)\t([^\t]+)\t\d\t([^\t]+)\t[^\t]+\t[^\t]+\t([^\t]+)\n')

#Title_ratings header #tconst	averageRating	numVotes
Ratings_info_regex = re.compile(r'tt\d{7}\t(\d\.\d)\t(\d+)\n')

```
Now to actually run the regular expressions and capture the data I want, I first created a dictionary to collect the Ids captured from the Id regex, and then read each line of data from Title_akas.txt to save memory and executed the search for Id's of Chinese titles.
```python
Chinese_titles_dict = {}

with open('Textfiles/Title_akas.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline() #reading line by line as loading in the whole file under with open.. too expensive on memory
        if line == '':
            break 
        Check_is_chinese = Chinese_titles_id_regex.search(line)
        if Check_is_chinese is not None:
            for i in range(1,5):
                if Check_is_chinese:
                    Chinese_id = Check_is_chinese.group(1)
                    Chinese_titles_dict[Chinese_id] = None  # dictionary because I don't want multiples

print("Done parsing for Chinese movies")

```
Next, I searched through Title_basics.txt to capture the desired data groups from the Chinese titles captured previously:
1. Primary Title
2. Original Title
3. Start year
4. Genres

```python
Chinese_movies = Chinese_titles_dict.keys()
Chinese_movies_dict = {}

with open('Textfiles/Title_basics.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Chinese_movies: # the previously captured Chinese titles
                    Basic_info = Basics_info_regex.search(line)
                    if Basic_info: # weeds out other titles such as shorts or tv shows, leaving movies
                        Genres = re.sub(',','&',Basic_info.group(4)) # replacing the commas separating genres to store all genres together
                        Basic_info = [Basic_info.group(1),Basic_info.group(2),
                                      Basic_info.group(3),Genres]
                        Chinese_movies_dict[Id]= Basic_info

print("Done writing Chinese movie info")
```
Starting by updating the list of Chinese movies to be only movie Ids and not all types of titles, I searched Title_ratings.txt and capture the average rating and the number of votes of Chinese movies.
```python
Chinese_movies = Chinese_movies_dict.keys()

with open('Textfiles/Title_ratings.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Chinese_movies:
                    Ratings_info = Ratings_info_regex.search(line)
                    if Ratings_info:
                        Chinese_movies_dict[Id].append(Ratings_info.group(1))
                        Chinese_movies_dict[Id].append(Ratings_info.group(2))
                        
print("Done rating Chinese movies")

```
Some of the captured Chinese movies' data is not complete, so I created a copy of the Chinese movie dictionary with the movie Id as the key and the other data as values to be able to remove the movies with incomplete data.
```python
Temp_dict = Chinese_movies_dict.copy()

for key,value in Chinese_movies_dict.items():
    if len(value)<=4:
        Temp_dict.pop(key)

Chinese_movies_dict = Temp_dict
```
All that is left is to save the Chinese movie dictionary as Chinese_movies.txt to be able to use it for analysis. Dictionaries in python do not display well when written to a text file, so I converted the dictionary to a sting, cleaned it up, and wrote to Chinese_movies.txt with a header of my data labels and the cleaned string.
```python
Chinese_movies_dict_str = str(Chinese_movies_dict)
Pretty_dict_str = Chinese_movies_dict_str.replace("{",'').replace("}",'').replace('"','').replace("'",'').replace(': [',',').replace('], ','\n').replace('\\N','N/A').replace('\\','').replace(']','')

with open('Textfiles/Chinese_movies.txt','w',encoding = 'utf8') as wf:
    wf.write("tconst\tprimaryTitle\toriginalTitle\tstartYear\tgenres\taverageRating\tnumVotes\n")
    wf.write(Pretty_dict_str)
print("Done!")
```
Supposedly, I now have only Chinese movie data according to IMDb's datasets. However upon inspection of Chinese_movies.txt, I notice that there are movies such as _Gone With the Wind_ and _Wuthering Heights_.
```
# from Chinese_movies.txt
tconst	primaryTitle	originalTitle	startYear	genres	averageRating	numVotes
tt0014429,Safety Last!, Safety Last!, 1923, Action&Comedy&Thriller, 8.1, 18750
tt0017925,The General, The General, 1926, Action&Adventure&Comedy, 8.1, 82447
...
tt0031381,Gone with the Wind, Gone with the Wind, 1939, Drama&History&Romance, 8.1, 293668
...
tt0032138,The Wizard of Oz, The Wizard of Oz, 1939, Adventure&Family&Fantasy, 8.0, 373691
tt0032145,Wuthering Heights, Wuthering Heights, 1939, Drama&Romance, 7.6, 16685

```
Upon pulling up IMDb's webpage and searching for their list of Chinese movies, the first movie that pops up on their list is 1917, which is not what I would consider to be a "Chinese" movie. IMDb includes movies that have been distributed in a certain country in their list of movies from said country, so as many movies have been distributed in China that are not movies from China, I had to verify that each movie that I collected from the datasets is actually from China.

### Verifying Chinese Movies
To verify that the data I have collected is of a movie from China, I scraped the IMDb page of each movie I collected using their title id. Before scraping from the title pages of IMDb, I checked to make sure that it is allowed in [IMDb.com/robots.txt](https://www.imdb.com/robots.txt), which it is. IMDb also has not set a crawl speed limit, so I let my urllib requests run as normal. In the IMDb pages for titles, they include the country of origin. So, I parsed through the HTML of the title pages to find the country of origin for each movie in my Chinese_movies.txt file, and if the result of the country-of-origin search showed that the movie originated from somewhere other than China, I dropped that movie from my data frame. After completing the scrape of the approximately 5,000 IMDb movie pages (which took over an hour the first time executed), my Chinese movie data frame reduced from 4,965 to 2,423, and I saved this verified Chinese movie data frame as Dataframe.txt.
```python
# code from verifying_movie_is_Chinese_scrape.py
# importing necessary libraries
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

Col_names = ['Id','Primary Title','Original Title','Year','Genres','Average Rating','# of Votes']
data = pd.read_csv('Textfiles/Chinese_movies.txt', delimiter = ",",header=0,names=Col_names,
                   error_bad_lines=False) #some movies don't have reviews->bad, not keeping those for analysis
# created dataframe from Chinese_movies.txt as easy to refer to specific values

Base_url = 'https://www.imdb.com/title/'   

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

data.to_csv('Textfiles/Dataframe.txt')
```
Now that I have collected all of the data I want about the movies themselves, it is time to collect the user reviews.

### Scraping User Reviews
User review data is not included in IMDb's available datasets--and from the size of their uncompressed datasets of much small info I can see why--so to gather the user reviews of Chinese movies, I had to scrape IMDb again. Scraping from the separate user reviews page of IMDb titles is also allowed, so I started off in an equivalent manner as when I scraped to verify the country-of-origin, except for changing the URL format. If the request to scrape from a specific movie's user reviews did not time out, which a handful did, I collected the user review itself, the user, the user rating, and the date of the review for all user reviews of that movie. Some reviews included spoilers, or did not have ratings, so mu code had to change a bit in its parsing through the HTML for the correct data to be collected.
```python
# code from scrape_IMDb_user_reviews.py
import urllib.request, pprint, re
from bs4 import BeautifulSoup
import pandas as pd

Base_url = 'https://www.imdb.com/title/'
End_url = '/reviews/'

data = pd.read_csv('Textfiles/Dataframe.txt', delimiter = ",")
data = data.drop(columns = 'Unnamed: 0') #don't need the index column
    
User_reviews_dict = {}
User_ratings_df = pd.DataFrame()

for i in range(len(data.index)):
    try:
        with urllib.request.urlopen(Base_url+data.at[i,'Id']+End_url,timeout=10) as request:
                soup = BeautifulSoup(request.read(),'lxml')
        try:
            User_reviews = soup.find_all('div', {'class': 'text show-more__control'})   
            # a list of user reviews # removed limit in hopes to improve topic models # call User_reviews[i].contents for individual reviews
            
            User_reviews_dict[data.at[i,'Id']] = {} 
            #creating nested dictionary {'id1':{0:'first review',1:'second review},'id2':{0:'first review of 2nd id',1:'second review of 2nd id}}...
            
            Ratings = []
            for j in range(len(User_reviews)):
                User_reviews_dict[data.at[i,'Id']][j] = User_reviews[j].text
                
            for k in range(len(User_reviews)):
                user_rating_num = data.at[i,'Id']+'_'+str(k)
                
                if len(User_reviews[k].parent.parent.contents)== 7: # no rating
                    rating = 'N/A'
                    user = User_reviews[k].parent.parent.contents[3].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[3].contents[2].text
                
                    
                if len(User_reviews[k].parent.parent.contents) == 11: # no rating & has spoiler
                    rating = 'N/A'
                    user = User_reviews[k].parent.parent.contents[3].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[3].contents[2].text

                    
                if len(User_reviews[k].parent.parent.contents) == 13: # has spoiler
                    rating = re.sub('\n','',User_reviews[k].parent.parent.contents[1].text)
                    user = User_reviews[k].parent.parent.contents[5].contents[1].text
                    date_posted = User_reviews[k].parent.parent.contents[5].contents[2].text

                    
                if len(User_reviews[k].parent.parent.contents) == 9:  # regular
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
```
After collecting the user review texts and organizing the other review and ratings data into a data frame, I saved the user reviews to User_reviews.txt and saved the data frame to User_ratings_dataframe.txt .
```python
with open('Textfiles/User_reviews.txt', 'w',encoding='utf8') as wf:
    wf.write(pprint.pformat(User_reviews_dict, depth=2))
    
User_ratings_df = User_ratings_df.rename(columns={0:'Id',1:'User',2:'Rating',3:'Date Posted'})
User_ratings_df.to_csv('Textfiles/User_ratings_dataframe.txt')
```
## Sentiment Analysis

### What is Sentiment Analysis?
Sentiment analysis is a natural language processing technique used in text analysis to evaluate subjective information in a source material and quantify the tone of the material. Sentiment analysis is widely used in social media monitoring to capture the public opinion and feeling held on certain topics, such as government policies or brands. Using the NLTK library, sentiment analysis is relatively simple to perform without needing an extensive background in programming.

### Sentiment Analysis of User Reviews
To perform sentiment analysis, there are a few necessary items to import and download.
```python
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
```
```python
mport re, numpy, textwrap
import pandas as pd


results = []
texts = []

with open('Textfiles/User_reviews.txt','r',encoding ='utf8') as rf:
    User_reviews = rf.read()
    
User_ratings_df = pd.read_csv('Textfiles/User_ratings_dataframe.txt') 
User_ratings_df = User_ratings_df.drop(columns = 'Unnamed: 0')

All_user_reviews_for_movie = re.split(r"'(tt\d{7})':", User_reviews)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    Ind_user_reviews = re.split(r"\W\W(\d+):\s\W",All_user_reviews_for_movie[i+1])[1:]
    if Ind_user_reviews != []:
        for j in range(0,len(Ind_user_reviews),2):
            review_contents = Ind_user_reviews[j+1]
            texts.append(textwrap.fill(review_contents))

```
[How I embedded the plotly visualizations](https://towardsdatascience.com/how-to-create-a-plotly-visualization-and-embed-it-on-websites-517c1a78568b)
Bar Chart of frequencies of User ratings for sample size 800.
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/9.embed"></iframe>
Dist of Compound SA scores of sample over time
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/11.embed"></iframe>
Box dist of SA score per User ratings
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/15.embed"></iframe>
Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

## Most Common Words in User Reviews

## Topic Modeling of User Reviews

### Topic Word Clouds
![Image](WC/Topic_0wordcloud.png)    ![Image](WC/Topic_1wordcloud.png)

### Markdown

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/stephcpalmer/IMDb_Chinese_title_user_reviews/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it ou
