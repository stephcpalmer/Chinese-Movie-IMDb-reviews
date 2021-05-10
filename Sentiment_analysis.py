import nltk
from nltk import classify
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re, numpy, textwrap
import pandas as pd
nltk.download('vader_lexicon')

results = []
texts = []

with open('User_reviews.txt','r',encoding ='utf8') as rf:
    User_reviews = rf.read()
    
User_ratings_df = pd.read_csv('User_ratings_dataframe.txt') 
User_ratings_df = User_ratings_df.drop(columns = 'Unnamed: 0')

All_user_reviews_for_movie = re.split(r"'(tt\d{7})':", User_reviews)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    Ind_user_reviews = re.split(r"\W\W(\d+):\s\W",All_user_reviews_for_movie[i+1])[1:]
    if Ind_user_reviews != []:
        for j in range(0,len(Ind_user_reviews),2):
            review_contents = Ind_user_reviews[j+1]
            texts.append(textwrap.fill(review_contents))
        
for i in range(len(texts)):
    pol_score = SIA().polarity_scores(texts[i])
    pol_score['headline'] = User_ratings_df.at[i,'Id'] 
    results.append(pol_score)
    
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

errors = []

for i in range(len(User_ratings_df.index)):
    if pd.isnull(User_ratings_df.at[i,'Rating']) is False:
        calculated_rating = User_ratings_df.at[i,'Compound_Score'] * .5 + .5
        actual_rating = eval(User_ratings_df.at[i,'Rating']) 
        error = (calculated_rating - actual_rating / actual_rating ) *100
        errors.append(error)
    if pd.isnull(User_ratings_df.at[i,'Rating']) is True:
        errors.append(numpy.nan)
        
User_ratings_df.insert(8,'Error',errors)

User_ratings_df.to_csv('User_ratings_df_with_SA_scores.txt')

from bokeh.plotting import figure, output_file, show
from random import sample

output_file("SA_Sample_Scores.html")

Score_sample = User_ratings_df.sample(100,axis='index')
source = ColumnDataSource(Score_sample)
hover = HoverTool(tooltips = 
                 [('Id','@Id'),('Compound Score','@Compound_Score'),('Rating','@Rating'),('Error','@Error %')])

q = figure(
   tools=[hover],
   title="Trial 2",
   y_axis_label='Sentiment Analysis Score'
)

q.scatter(x = 'index', y = 'Compound_Score', source = source,
         legend_label="Compound Sentiment Analysis Score", size=8)
q.xaxis.visible = False

show(q)