# Objective
In this project I aim to analyze user reviews of Chinese movies from the IMDb website and draw some inferences about the western audience's perception of Chinese cinema.

# Motivation
This project is the final project of Professor Vierthaler's Spring 2021 CHIN 303 "Hacking Chinese Studies" class at William & Mary. From the time I was in high school, I have been beguiled by Chinese tv shows and movies. This interest in Chinese programs lead to me taking over 20 Chinese Studies credits at William & Mary even though most of them did not satisfy any of my liberal arts requirements. Thankfully, in my last semester at the College, I have found a class that intersects my academic focus in Applied Mathematics and my interest in Chinese language and culture. Hence, in the final project I wished to analyze Chinese movies, and since I am aware of IMDb's available datasets, and in my previous programming classes I have not learned how to web scrape, my ideas manifested as sourcing my analysis of Chinese movie user reviews from IMDb.

# Data Gathering and Cleaning
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
# Analysis of User Review Data

## Sentiment Analysis
### What is Sentiment Analysis?
Sentiment analysis is a natural language processing technique used in text analysis to evaluate subjective information in a source material and quantify the tone of the material. Sentiment analysis is widely used in social media monitoring to capture the public opinion and feeling held on certain topics, such as government policies or brands. Using the NLTK library, sentiment analysis is relatively simple to perform without needing an extensive background in programming.

### Sentiment Analysis of User Reviews
The most popular natural language processing library for python is NLTK, the Natural Language Toolkit. From NLTK, the VADER lexicon must be downloaded in order to perform sentiment analysis.

```python
# code from Sentiment_analysis.py
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
```
As I have stored the user reviews in a text file and other data about the user review in a data frame, I must also import the libraries necessary to access my data. If you are performing sentiment analysis of a simple string located in the local python script, this is not necessary.
```python
mport re, numpy, textwrap
import pandas as pd
```
The texts of the user reviews in User_reviews.txt are stored in the following format: {'id': {'review # for movie': 'review text'}}. In order to form a list of just the text of the reviews, I needed to split the text file using regular expressions. First, I split the text file into each movie id and its corresponding user reviews. Then, once I was able to operate within the reviews of a single movie, if a review was detected, I added each review to the list of texts by iterating through all of the reviews for the specific movie. Since the user review was formatted in a dictionary style in the text file using pprint, it had indentations. So, I used textwrap to fill in the space of the hanging indent after the first line of each review to make the text of individual reviews a bit more legible before appending them to the list of texts.
```python
texts = []

with open('Textfiles/User_reviews.txt','r',encoding ='utf8') as rf:
    User_reviews = rf.read()
    
User_ratings_df = pd.read_csv('Textfiles/User_ratings_dataframe.txt') 
User_ratings_df = User_ratings_df.drop(columns = 'Unnamed: 0')

All_user_reviews_for_movie = re.split(r"'(tt\d{7})':", User_reviews)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    Ind_user_reviews = re.split(r"\W\W(\d+):\s\W",All_user_reviews_for_movie[i+1])[1:]
    if Ind_user_reviews != []: # some movies don't have reviews
        for j in range(0,len(Ind_user_reviews),2):
            review_contents = Ind_user_reviews[j+1]
            texts.append(textwrap.fill(review_contents))
```
Now that I have made a list of the texts of user reviews I wish to analyze, I can iterate through this list and get the sentiment analysis scores for each user review. Sentiment Intensity Analyzer or SIA, the tool performing the sentiment analysis, outputs four different scores: the positive, negative, neutral, and compound. I will only use the compound score, which is a normalized, aggregate score from the user review. If it is close to 1, the review has been analyzed to have a strong positive tone. If it close to - 1, the user review has been analyzed to have strong negative tone. If the compound score is close to 0, it does not have a strong tone either way.
```python
results = []
for i in range(len(texts)):
    pol_score = SIA().polarity_scores(texts[i])
    pol_score['headline'] = User_ratings_df.at[i,'Id'] 
    results.append(pol_score)
```
I added all of the scores for every review into the current data frame User_ratings_df. Although I will only look at the compound score for analysis, if I return to expand on this project, I am interested in storing that information for future analysis.
```python
pos_scores = []
neu_scores = []
neg_scores = []
com_scores = []

for i in range(len(results)):
    pos_scores.append(results[i]['pos'])
    neu_scores.append(results[i]['neu'])
    neg_scores.append(results[i]['neg'])
    com_scores.append(results[i]['compound'])
    
User_ratings_df.insert(4,'Negativity_Score',neg_scores)
User_ratings_df.insert(5,'Neutrality_Score',neu_scores)
User_ratings_df.insert(6,'Positivity_Score',pos_scores)
User_ratings_df.insert(7,'Compound_Score',com_scores)
```
With these sentiment analysis scores in my data frame, I compared them with the rating that each reviewer left along with their review of the movie. As I scraped the user ratings in string form, I had to evaluate the string to get a number. As the IMDb user rating system is from 1-10/10, the evaluated ratings outputted as 0 - 1. Thus, to make the compound sentiment analysis score equivalent to the user rating's range, I manipulated it using a simple math equation so that a score of 0 would be transformed to 0.5, -1 would be transformed to 0, and a score of 1 will stay 1. With the transformed user rating and compound sentiment score, I calculated the percent error of VADER's compound score. If the reviewer did not leave a rating with their review, I used the numpy library's nan constant to still represent that data as null instead of failing to append to the overall lists of errors and evaluated ratings to make placing these data points into the data frame easier.
```python
errors = []
ratings_eval = []
for i in range(len(User_ratings_df.index)):
    if pd.isnull(User_ratings_df.at[i,'Rating']) is False:
        actual_rating = eval(User_ratings_df.at[i,'Rating'])
        ratings_eval.append(actual_rating)
        calculated_rating = User_ratings_df.at[i,'Compound_Score'] * .5 + .5
        error = (calculated_rating - actual_rating / actual_rating ) *100
        errors.append(error)
    if pd.isnull(User_ratings_df.at[i,'Rating']) is True:
        errors.append(numpy.nan)
        ratings_eval.append(numpy.nan)
        
User_ratings_df.insert(8,'Error',errors)
User_ratings_df.insert(9,'Evaluated_User_Rating',ratings_eval)
User_ratings_df.to_csv('Textfiles/User_ratings_df_with_SA_scores.txt')
```
Time to visualize the data! As I have approximately 8,000 user reviews, any plot I made looked too hectic, so for my visualizations I only pulled the data from a sample of the population of my data. From a past statistics class, I learned a rule-of-thumb for choosing a sample size of at least 10% the population for a representative sample, so the size I chose for my sample using pandas' Data Frame sample function is 800. I saved this sample data frame Score_sample to a text file.
```python
Score_sample = User_ratings_df.sample(800,axis='index',random_state=1)
Score_sample.to_csv('Textfiles/Sample_user_ratings_df_with_SA_scores.txt')
```
I first plotted the counts of the different user ratings from the sample.

<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/9.embed"></iframe>

The distribution of sampled user ratings is unimodal and skewed to the left with the lowest rating count a bit higher than if it were to be perfectly skewed to the left. You can hover over the bars of the graph to the exact counts. To create this graph, I used Plotly, a python library for data visualizations. Plotly also has online functionality for creating data visualizations with [Chart Studio](https://plotly.com/chart-studio/). With a free account you can create publicly accessible visualizations, but if your data is too large it is better to use it through python as it will not work online. For example, though I created this bar chart in python, I was able to quickly recreate it using Chart Studio, but when I tried to create a visualization using my whole data frame instead of a sample on Chart Studio, it did not work. 

Although creating this bar chart is much quicker in Chart Studio, it was not hard to create in python. First, I had to count the occurrences of each user rating level. Pandas Data Frame has a handy count function, so I called it from locating every occurrence of a certain rating level. Then I created a data frame of just the rating levels and their counts.
```python
counts = []
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.1,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.2,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.3,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.4,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.5,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.6,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.7,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.8,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==0.9,'Evaluated_User_Rating'].count())
counts.append(Score_sample.loc[Score_sample.Evaluated_User_Rating==1.0,'Evaluated_User_Rating'].count())

Bar_df = pd.DataFrame(data=
                      [(0.1,counts[0]),(0.2,counts[1]),(0.3,counts[2]),(0.4,counts[3]),(0.5,counts[4]),(0.6,counts[5]),
                       (0.7,counts[6]),(0.8,counts[7]),(0.9,counts[8]),(1.0,counts[9])],columns=['Evaluated_User_Rating','Count'])
```
To create the bar chart, I had to import Plotly and using their built-in express, creating figures is very simple. I used the data frame formed previously as the source of the data for the figure, and by referencing the column names I was able to set my axes accordingly. I updated the x axis to show all the distinct levels of ratings instead of having the default few labelled. I also made a few other stylistic choices such as manipulating the lines and tick marks of the axes.
```python
import plotly.express as px

fig = px.bar(Bar_df, x='Evaluated_User_Rating',y='Count',title='User Rating Counts of Sample')
fig.update_xaxes(showline=True, linecolor='black',
                showticklabels=True,nticks=11,ticks='outside',
                title_text='User Rating')
fig.update_yaxes(showline=True, linecolor='black',
                nticks=12,ticks='outside')
fig.show()
```
Onto visualizing the compound sentiment analysis scores of the user reviews!

<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/11.embed"></iframe>

They are distributed concentrated at both extremes, +1 and -1, with few in the range [-0.5,0.5]. Thus, VADER has found that most of the user reviews convey a strong tone, mostly a strong positive tone, but also a fair amount of strong negative reviews. Hovering over individual points (you can also use the tools on the top of the plot to look at the data points more closely) shows the unique review Id of the data point and the date the review was posted. The data points go from earliest on the left to most recent on the right, and in the most recent years, I would discern that the ratings are a bit more varied, especially compared to reviews between 2011-2017. This may be attributed to the western audience being more aware of international movies, and thus there are more people reviewing Chinese movies on IMDb. There does not seem to be a marked recent increase in interest towards Chinese movies specifically according to my research, but maybe plotting this data for movies of other countries may show this to be the case.

To create this figure, I had to transform the Date Posted data strings into datetime format, also made convenient by pandas. Creating a scatter plot of the compound scores over time was also straightforward following the Plotly [documentation](https://plotly.com/python-api-reference/generated/plotly.express.scatter).
```python
dates_formatted = []
for i in Score_sample.index:
    date_form = pd.to_datetime(Score_sample.at[i,'Date Posted']).date().strftime('%Y/%m/%d')
    dates_formatted.append(date_form)
Score_sample.insert(10,'Date Formatted',dates_formatted)  # new column for formatted dates
Dist_df = Score_sample.sort_values(by=['Date Formatted']) #sorting the data frame by date oldest-> newest

fig2 = px.scatter(Dist_df,x='Date Formatted',y='Compound_Score',hover_name="Id",title='Distribution of Sample Compound SA Scores')
fig2.update_xaxes(showticklabels=False,visible = False) # too distracting to show dates
fig2.update_yaxes(showticklabels=True,nticks=12,ticks='inside',
                  showline=True, linecolor='black',
                  showgrid=True,title_text= 'Compound SA Score',
                  zeroline=True, zerolinecolor='black', zerolinewidth=.1) # line at horizontal center of plot
fig2.show()
```
Now to visualize the distribution of compound score for each rating level via box plot.

<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/15.embed"></iframe>

The compound scores for high ratings are remarkably more concentrated at the upper end of the score range, and the opposite is true for low ratings. Suitably so, the middle level rating of 0.5 has the largest range of (-0.99,0.99) and inter-quartile range (-0.74,0.96) which is visible when hovering over a box. As noted previously, the compound score is above all things a marker for the  strength of tone, so a review with rating 0.5, where the reviewer does not hold a strong opinion of the movie either way, is expected to land in the middle of the compound score range region of (-0.5,0.5). Also, it is worth noting that the median compound score for the bottom two rating levels 0.1 and 0.2 are not that different considering the bar chart which showed a large number of the lowest rating compared to the second lowest rating. I suppose that once you hold a negative opinion of a movie, it is natural to give it the worst rating possible, versus trying to find a possible merit in the movie to give it a higher score.

The python code to create the box plot:
```python
fig3 = px.box(Score_sample,x='Evaluated_User_Rating',y='Compound_Score',hover_name="Id",
              title='Distribution of Compound Sentiment Analysis Score for User Ratings')
fig3.update_xaxes(showticklabels=True,nticks=11,title_text='User Rating')
fig3.update_yaxes(showticklabels=True,nticks=12,ticks='inside',
                  showline=True, linecolor='black',
                  showgrid=True,title_text= 'Compound SA Score')
fig3.show()
py.plot(fig3, filename = 'Box dist of SA score per User ratings', auto_open=True)
```
## Most Common Words in User Reviews
NLTK can also be used to find the most common words in a text using the FreqDist class.

```python
# code from Freq_dist.py
import nltk
from nltk.corpus import stopwords 
import string #to pull out punctuations
nltk.download('stopwords')  
nltk.download('punkt')  #word tokenizer

texts = ''
stopwords = set(stopwords.words('english')) #set of very common english words

with open('Textfiles/User_reviews.txt','r',encoding ='utf8') as rf:
    text = rf.read()
    
All_user_reviews_for_movie = re.split(r"'(tt\d{7})': \{", text)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        texts+=review_contents
```
After importing the necessary libraries, downloading NLTK modules for word tokenization and stopwords, and setting up a single string that includes all user reviews we can call to FreqDist and create a frequency distribution of all the words used in the corpus of user reviews.
```python
fd = nltk.FreqDist()
for sent in nltk.sent_tokenize(texts):  # sent tokenize splits the single texts string into sentences
    for word in nltk.word_tokenize(sent): # word tokenize splits each sentence into words
        if word.lower() not in stopwords and word not in set(string.punctuation): # if word is not already in stopwords set and is not puntuation
            fd[word.lower()]+=1 # add to the frequency of certain word
fd.most_common(100) #prints list with sets containing the 100 most common words and their frequencies in sets
```
The resulting output shows the most common words in the user reviews.
```
[('``', 59611),("'s", 16577),('movie', 13320),('film', 11806),("''", 7848),("n't", 7416),("'the", 6565),
...('beautiful', 1005),('family', 1000),('martial', 998),('actually', 996),('look', 990)]
```
## Topic Modeling of User Reviews
Topic modeling is a text analysis technique to capture the abstract topics of a corpora. To further analyze the user reviews of Chinese movies I created an LDA topic model, which trained over my corpus of user reviews. The code to my topic model can be viewed in my repository in the file Topic_model_id_reviews.py . Using the tokenized user reviews, I created a 4-topic model. The Word Clouds for each topic are below.

                                Topic #0
![Image](WC/Topic_0wordcloud.png)    

                                Topic #1
![Image](WC/Topic_1wordcloud.png)\

                                Topic #2
![Image](WC/Topic_2wordcloud.png)

                                Topic #3
![Image](WC/Topic_3wordcloud.png)
### Word Embeddings

