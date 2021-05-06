import pandas as pd
import nltk
from nltk.corpus import stopwords


texts = ''

stopwords = set(stopwords.words('english'))

with open('User_reviews.txt','r',encoding ='utf8') as rf:
    text = rf.read()
    
All_user_reviews_for_movie = re.split(r"'(tt\d{7})': \{", text)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        texts+=review_contents
        
fd = nltk.FreqDist()
for sent in nltk.sent_tokenize(texts):
    for word in nltk.word_tokenize(sent):
        fd[word.lower()]+=1
fd.plot(50,cumulative=False) 

