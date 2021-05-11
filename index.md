## Objective
In this project I aim to analyze user reviews of Chinese movies from the IMDb website and draw some inferences about the western audience's perception of Chinese cinema.

## Motivation
This project is the final project of Professor Vierthaler's Spring 2021 CHIN 303 "Hacking Chinese Studies" class at William & Mary. From the time I was in high school, I have been beguiled by Chinese tv shows and movies. This interest in Chinese programs lead to me taking over 20 Chinese Studies credits at William & Mary even though most of them did not satisfy any of my liberal arts requirements. Thankfully, in my last semester at the College, I have found a class that intersects my academic focus in Applied Mathematics and my interest in Chinese language and culture. Hence, in the final project I wished to analyze Chinese movies, and since I am aware of IMDb's available datasets, and in my previous programming classes I have not learned how to web scrape, my ideas manifested as sourcing my analysis of Chinese movie user reviews from IMDb.

## IMDb Data
I first pulled data from IMDb's datasets to identify IMDb's Chinese movies.

### Downloading and Unzipping IMDb Datasets

IMDb has subsets of their data [available](https://www.imdb.com/interfaces/) for personal and non-commercial use. I downloaded the data from three of their datasets: title.akas, title.basics, and title.ratings by using the urllib package for Python.

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

#titleId	ordering	title	region	language	types	attributes	isOriginalTitle
Chinese_titles_id_regex = re.compile(r'(tt\d{7}).+\tCN\t',re.X) #captures id if the title is from China
Id_regex = re.compile(r'(tt\d{7})')

#tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres  ###Header from Title_basics.txt
Basics_info_regex = re.compile(r'tt\d{7}\tmovie\t([^\t]+)\t([^\t]+)\t\d\t([^\t]+)\t[^\t]+\t[^\t]+\t([^\t]+)\n')

#tconst	averageRating	numVotes
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
                        Basic_info = [Basic_info.group(1),Basic_info.group(2),Basic_info.group(3),Genres]
                        Chinese_movies_dict[Id]= Basic_info

print("Done writing Chinese movie info")
```
### Word Clouds
![Image](WC/Topic_0wordcloud.png)

### Markdown
[How I embedded the plotly visualizations](https://towardsdatascience.com/how-to-create-a-plotly-visualization-and-embed-it-on-websites-517c1a78568b)
Bar Chart of frequencies of User ratings for sample size 800.
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/9.embed"></iframe>
Dist of Compound SA scores of sample over time
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/11.embed"></iframe>
Box dist of SA score per User ratings
<iframe width="590" height="400" frameborder="0" scrolling="no" src="//plotly.com/~StephCPalmer/15.embed"></iframe>
Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/stephcpalmer/IMDb_Chinese_title_user_reviews/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it ou
