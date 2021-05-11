## Objective
In this project I aim to analyze user reviews of Chinese movies from the IMDb website and draw some inferences about the western audience's perception of Chinese cinema.

## Motivation
This project is the final project of Professor Vierthaler's Spring 2021 CHIN 303 "Hacking Chinese Studies" class at William & Mary. From the time I was in high school, I have been beguiled by Chinese tv shows and movies. This interest in Chinese programs lead to me taking over 20 Chinese Studies credits at William & Mary even though most of them did not satisfy any of my liberal arts requirements. Thankfully, in my last semester at the College, I have found a class that intersects my academic focus in Applied Mathematics and my interest in Chinese language and culture. Hence, in the final project I wished to analyze Chinese movies, and since I am aware of IMDb's available datasets, and in my previous programming classes I have not learned how to web scrape, my ideas manifested as sourcing my analysis of Chinese movie user reviews from IMDb.

## Gathering Data

### IMDb Datasets

IMDb has subsets of their data [available](https://www.imdb.com/interfaces/) for personal and non-commercial use. I downloaded the data from three of their datasets: title.akas, title.basics, and title.ratings by using the urllib package for Python.

```
import urllib.request

#retrieve zipped files

Title_akas_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.akas.tsv.gz','Title_akas.tsv.gz')
Title_basics_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.basics.tsv.gz','Title_basics.tsv.gz')
Title_ratings_request = urllib.request.urlretrieve('https://datasets.imdbws.com/title.ratings.tsv.gz','Title_ratings.tsv.gz')

```

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
