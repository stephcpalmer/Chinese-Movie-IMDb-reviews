import gensim, nltk, re
from gensim.models import Word2Vec
from nltk.corpus import stopwords

with open('Textfiles/User_reviews.txt','r',encoding ='utf8') as rf:
    text = rf.read()
 
labels = []
texts = []
stopwords = set(stopwords.words('english'))
top_100_words = ['``', "'s",'movie','film', "''", "n't", "'the", 'one', 'story', 'like', 'good', 'time',
 'also', "'and", 'even', 'really', 'would', 'well', 'much', 'see', 'people', 'love', 'action', 'characters', 'great',
 'movies', 'first', 'many', 'life', "'of", 'way', 'watch', 'scenes', 'could', 'two', 'get', 'films', "'to", 'make', 'made',
 'character', 'plot', '...', 'director', 'little', "'is", 'know', 'still', 'bad', 'think', 'end', 'man', 'acting', 'best',
 "'that", "'in", 'better', 'quite', 'scene', "'this", 'seen', 'never', 'though', 'li', 'zhang', 'years', 'go', "'movie",
 'real', 'world', 'part', 'lot', 'new', 'young', 'say', 'something', 'back', 'actors', 'feel', 'old', 'may',
 'watching', 'another', 'work', 'long', 'however', 'us', 'bit', 'find', 'makes', "'m", "'with", 'war', 'beautiful', 'family',
 'martial', 'actually', 'look'] #removed china and chinese for analysis
stopwords.update(top_100_words)

All_user_reviews_for_movie = re.split(r"'(tt\d{7})': \{", text)[1:]

for i in range(0, len(All_user_reviews_for_movie), 2):
    print(i)
    id_num = All_user_reviews_for_movie[i]
    labels.append(id_num)
    Ind_user_reviews = re.split(r"(\d:) '",All_user_reviews_for_movie[i+1])[1:]
    
    for i in range(0,len(Ind_user_reviews),2):
        review_contents = Ind_user_reviews[i+1]
        sentences = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(review_contents)]
        refined_sentences = []
        for sentence in sentences:
            refined_sentences.append([word.lower() for word in sentence if word.isalpha() and word not in stopwords])
        texts.extend(refined_sentences)
 
word2vecModel = Word2Vec(texts)
word2vecModel.save("modelfile.model")

word2vecModel.wv.most_similar("japanese")
word2vecModel.wv.most_similar("arts")
word2vecModel.wv.most_similar("father")

