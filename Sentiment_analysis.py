from nltk import classify
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re, textwrap

nltk.download('vader_lexicon')


results = []

texts = []


with open('User_reviews.txt','r',encoding ='utf8') as rf:
    text = rf.read()
    
All_user_reviews_for_movie = re.split(r"'(tt\d{7})': \{", text)[1:]

#for i in range(0, len(All_user_reviews_for_movie), 2):
for i in range(1):
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        texts.append(textwrap.fill(review_contents))


results = []
for i in range(len(texts)):
    pol_score = SIA().polarity_scores(texts[i]) # run analysis
    pol_score['headline'] = i # add headlines for viewing
    results.append(pol_score)

results
