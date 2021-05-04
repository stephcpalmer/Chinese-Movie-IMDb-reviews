#sentiment analysis # From programming historian's lesson on sentiment analysis
import nltk, re, os
import pandas as pd
import gensim
from gensim.models import ldamodel
from gensim.test.utils import datapath
nltk.download('stopwords')
from nltk.corpus import stopwords

#nltk.download('vader_lexicon')
#nltk.download('punkt')


labels = []
texts = []
stopwords = set(stopwords.words('english'))
movie_words = ['the','movie','film','story','china']
stopwords.update(movie_words)


lemmatizer = nltk.WordNetLemmatizer()

with open('1_user_reviews.txt','r',encoding='utf8') as rf:
    text = rf.read()
    
dataframe = pd.read_csv('Dataframe.txt', delimiter = ",")

dataframe = dataframe.drop(0)
user_review = re.split(r'\': \'', text)
print(len(user_review))

for i in range(0, len(user_review), 2):
    id_num = user_review[i]
    review_text = user_review[i+1]

    labels.append(id_num)

    tokenized_text = nltk.word_tokenize(review_text)

    refined = [word.lower() for word in tokenized_text if word.isalnum() and word.lower() not in stopwords]
    texts.append(refined)

corpus_dictionary = gensim.corpora.Dictionary(texts)
processed_corpus = [corpus_dictionary.doc2bow(review) for review in texts]

lda_model = gensim.models.ldamodel.LdaModel(corpus=processed_corpus, id2word=corpus_dictionary, 
                        iterations = 50,num_topics= 16)
temp_file = datapath("model")
lda_model.save(temp_file)

corpus_lda = lda_model[processed_corpus]
topics = lda_model.show_topics(num_topics=16, num_words=5)
print(topics)

#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#sid = SentimentIntensityAnalyzer()

#scores = sid.polarity_scores(user_review[1])
#for key in sorted(scores):
#        print('{0}: {1}, '.format(key, scores[key]), end='')


