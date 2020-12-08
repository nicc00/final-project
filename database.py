import pandas as pd

basics = pd.read_csv("datasets/title.basics.tsv", sep='\t', low_memory=False)
ratings = pd.read_csv("datasets/title.ratings.tsv", sep='\t')

data = pd.merge(basics, ratings, on ="tconst")

movies = data[data['titleType'] == 'movie']
movies = movies[movies['isAdult'] == 0]
movies = movies[~movies.genres.str.contains('Adult')]
