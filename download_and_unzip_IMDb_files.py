import urllib.request
import gzip

#retrieve zipped files

Title_akas_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.akas.tsv.gz','Title_akas.tsv.gz')
Title_basics_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.basics.tsv.gz','Title_basics.tsv.gz')
Title_ratings_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.ratings.tsv.gz','Title_ratings.tsv.gz')

#open zipped files

with gzip.open('Textfiles/Title_akas.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_akas.txt','wb') as w:
        w.writelines(myzip)

with gzip.open('Textfiles/Title_basics.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_basics.txt','wb') as w:
        w.writelines(myzip)

with gzip.open('Textfiles/Title_ratings.tsv.gz','rb') as myzip:
    with open('Textfiles/Title_ratings.txt','wb') as w:
        w.writelines(myzip)

