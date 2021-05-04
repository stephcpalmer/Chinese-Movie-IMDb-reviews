#sentiment analysis # From programming historian's lesson on sentiment analysis
import nltk, re, os
import pandas as pd
nltk.download('vader_lexicon')
nltk.download('punkt')

user_review = re.split(r'\': \'', text)

labels = []
texts = []
stopwords = []

lemmatizer = nltk.WordNetLemmatizer()

with open("User_reviews.txt",'r',encoding='utf8') as rf:
    text = rf.read()
dataframe = pd.read_csv('Dataframe.txt', delimiter = ",")

for i in range(0, len(user_review), 2):
    id_num = user_review[i]
    view_text = user_review[i+1]

    labels.append(id_num)

    tokenized_text = nltk.word_tokenize(text)

    refined = [word.lower() for word in tokenized_text if word.isalnum() and word not in stopwords]

    texts.append(refined)

path_to_mallet = os.path.join("mallet-2.0.8", "bin", "mallet")

lda_model = gensim.models.ldamallet.LdaMallet(path_to_mallet, 
                        corpus=processed_corpus, id2word=corpus_dictionary, 
                        num_topics=number_of_topics, optimize_interval=50, 
                        prefix='MovieReviews')

corpus_lda = lda_model[processed_corpus]
topics = lda_model.show_topics(num_topics=16, num_words=5)


#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#sid = SentimentIntensityAnalyzer()

#scores = sid.polarity_scores(user_review[1])
#for key in sorted(scores):
#        print('{0}: {1}, '.format(key, scores[key]), end='')


