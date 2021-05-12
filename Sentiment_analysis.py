import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

import re, numpy, textwrap
import pandas as pd


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

results = []     
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
ratings_eval = []
for i in range(len(User_ratings_df.index)):
    if pd.isnull(User_ratings_df.at[i,'Rating']) is False:
        calculated_rating = User_ratings_df.at[i,'Compound_Score'] * .5 + .5
        actual_rating = eval(User_ratings_df.at[i,'Rating'])
        ratings_eval.append(actual_rating)
        error = (calculated_rating - actual_rating / actual_rating ) *100
        errors.append(error)
    if pd.isnull(User_ratings_df.at[i,'Rating']) is True:
        errors.append(numpy.nan)
        ratings_eval.append(numpy.nan)
        
User_ratings_df.insert(8,'Error',errors)
User_ratings_df.insert(9,'Evaluated_User_Rating',ratings_eval)
User_ratings_df.to_csv('Textfiles/User_ratings_df_with_SA_scores.txt')


Score_sample = User_ratings_df.sample(800,axis='index',random_state=1)
Score_sample.to_csv('Textfiles/Sample_user_ratings_df_with_SA_scores.txt')

###Bar Plot###
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

import plotly.express as px


fig = px.bar(Bar_df, x='Evaluated_User_Rating',y='Count',title='User Rating Counts of Sample')
fig.update_xaxes(showline=True, linecolor='black',showticklabels=True,nticks=11,ticks='outside',title_text='User Rating')
fig.update_yaxes(showline=True, linecolor='black',nticks=12,ticks='outside')
fig.show()

### Needed to embed fig into GitHub Page
import chart_studio.tools as tls
import chart_studio.plotly as py

username = 'StephCPalmer' 
api_key = 'M8qEVu1mK0DQ8urtCkuk'
tls.set_credentials_file(username=username, api_key=api_key)
py.plot(fig, filename = 'User_Rating_Counts_of_Sample', auto_open=True)

###Scatter Plot###
dates_formatted = []
for i in Score_sample.index:
    date_form = pd.to_datetime(Score_sample.at[i,'Date Posted']).date().strftime('%Y/%m/%d')
    dates_formatted.append(date_form)
Score_sample.insert(10,'Date Formatted',dates_formatted)

Dist_df = Score_sample.sort_values(by=['Date Formatted'])

fig2 = px.scatter(Dist_df,x='Date Formatted',y='Compound_Score',hover_name="Id",title='Distribution of Sample Compound SA Scores')
fig2.update_xaxes(showticklabels=False,visible = False)
fig2.update_yaxes(showticklabels=True,nticks=12,ticks='inside',
                  showline=True, linecolor='black',
                  showgrid=True,title_text= 'Compound SA Score',
                  zeroline=True, zerolinecolor='black', zerolinewidth=.1)
fig2.show()
### for embedding
py.plot(fig2, filename = 'Distribution of Sample Compound SA Scores', auto_open=True)

###Box Plot###
fig3 = px.box(Score_sample,x='Evaluated_User_Rating',y='Compound_Score',hover_name="Id",
              title='Distribution of Compound Sentiment Analysis Score for User Ratings')
fig3.update_xaxes(showticklabels=True,nticks=11,title_text='User Rating')
fig3.update_yaxes(showticklabels=True,nticks=12,ticks='inside',
                  showline=True, linecolor='black',
                  showgrid=True,title_text= 'Compound SA Score')
fig3.show()
py.plot(fig3, filename = 'Box dist of SA score per User ratings', auto_open=True)



