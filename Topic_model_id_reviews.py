#sentiment analysis # From programming historian's lesson on sentiment analysis and class notes
import nltk, re
import pandas as pd
import gensim
from gensim.test.utils import datapath
from nltk.corpus import stopwords


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

  

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


labels = []
texts = []
stopwords = set(stopwords.words('english'))
top_100_words = ['``', "'s",'movie','film', "''", "n't", "'the", 'one', 'story', 'like', 'chinese', 'good', 'china', 'time',
 'also', "'and", 'even', 'really', 'would', 'well', 'much', 'see', 'people', 'love', 'action', 'characters', 'great',
 'movies', 'first', 'many', 'life', "'of", 'way', 'watch', 'scenes', 'could', 'two', 'get', 'films', "'to", 'make', 'made',
 'character', 'plot', '...', 'director', 'little', "'is", 'know', 'still', 'bad', 'think', 'end', 'man', 'acting', 'best',
 "'that", "'in", 'better', 'quite', 'scene', "'this", 'seen', 'never', 'though', 'li', 'zhang', 'years', 'go', "'movie",
 'real', 'world', 'part', 'lot', 'new', 'young', 'say', 'something', 'back', 'actors', 'feel', 'old', 'may',
 'watching', 'another', 'work', 'long', 'however', 'us', 'bit', 'find', 'makes', "'m", "'with", 'war', 'beautiful', 'family',
 'martial', 'actually', 'look']
stopwords.update(top_100_words)

with open('User_reviews.txt','r',encoding ='utf8') as rf:
    text = rf.read()
    
dataframe = pd.read_csv('Dataframe.txt', delimiter = ",")
dataframe = dataframe.drop(0)

All_user_reviews_for_movie = re.split(r"'(tt\d{7})': \{", text)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    id_num = All_user_reviews_for_movie[i]
    labels.append(id_num)
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        tokenized_text = []
        for sent in nltk.sent_tokenize(review_contents):
            words = nltk.word_tokenize(sent)
            for word in words:
                tokenized_text.append(word)
        refined = [word.lower() for word in tokenized_text if word.isalpha() and word.lower() not in stopwords]
        texts.append(refined)
    '''Original
    id_num = All_user_reviews_for_movie[i]
    labels.append(id_num)
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    review_texts = ''
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        review_texts = review_texts+review_contents  
    tokenized_text = []
    for sent in nltk.sent_tokenize(review_texts):
        words = nltk.word_tokenize(sent)
        for word in words:
            tokenized_text.append(word)
    refined = [word.lower() for word in tokenized_text if word.isalpha() and word.lower() not in stopwords]
    texts.append(refined)'''

#print(texts)
corpus_dictionary = gensim.corpora.Dictionary(texts)
corpus_dictionary.filter_extremes(no_below=5, no_above=.5)

processed_corpus = [corpus_dictionary.doc2bow(review) for review in texts]

from gensim.models import ldamodel

lda_model_1 = ldamodel.LdaModel(corpus=processed_corpus, 
                                            id2word=corpus_dictionary, 
                                            num_topics= 4,
                                            passes = 30,
                                            chunksize= 1000)

print('\nPerplexity: ', lda_model_1.log_perplexity(processed_corpus))
#temp_file = datapath("model")
#lda_model_1.save(temp_file)
'''
from wordcloud import WordCloud
import matplotlib.pyplot as plt
for i in range(lda_model_1.num_topics):
    plt.figure()
    plt.imshow(WordCloud().fit_words(dict(lda_model_1.show_topic(i, 50))))
    plt.axis("off")
    plt.title("Topic #" + str(i))
    plt.show()
    
'''  
from gensim.models.coherencemodel import CoherenceModel

cm1 = CoherenceModel(model=lda_model_1,corpus=processed_corpus,dictionary=corpus_dictionary,coherence='u_mass')
print(cm1.get_coherence())
'''
lda_model_2 = ldamodel.LdaModel(corpus=processed_corpus, 
                                            id2word=corpus_dictionary, 
                                            num_topics= 5,
                                            passes = 30,
                                            chunksize= 1000)

print('\nPerplexity: ', lda_model_2.log_perplexity(processed_corpus))



temp_file = datapath("model2")
lda_model_2.save(temp_file)

corpus_lda = lda_model_1[processed_corpus]
topics = lda_model_1.show_topics(num_topics=5, num_words=10)
print(topics)



    
for i in range(lda_model_2.num_topics):
    plt.figure()
    plt.imshow(WordCloud().fit_words(dict(lda_model_2.show_topic(i, 50))))
    plt.axis("off")
    plt.title("Topic #" + str(i))
    plt.show()
    
from gensim.models.coherencemodel import CoherenceModel

cm1 = CoherenceModel(model=lda_model_1,corpus=processed_corpus,dictionary=corpus_dictionary,coherence='u_mass')
cm2 = CoherenceModel(model=lda_model_2,corpus=processed_corpus,dictionary=corpus_dictionary,coherence='u_mass')

print(cm1.get_coherence(),cm2.get_coherence())'''




