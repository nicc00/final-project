import pandas as pd
import math

basics = pd.read_csv("datasets/title.basics.tsv", sep='\t', low_memory=False)
ratings = pd.read_csv("datasets/title.ratings.tsv", sep='\t')

data = pd.merge(basics, ratings, on ="tconst")

movies = data[data['titleType'] == 'movie']
movies = movies[movies['isAdult'] == 0]
movies = movies[~movies.genres.str.contains('Adult')]
movies = movies[~movies.startYear.str.contains('N')]
movies.startYear = movies.startYear.astype(int)
popularity = []
for i in range(len(movies)):
    score = math.ceil((len(movies) - i) / (len(movies) / 10))
    popularity.append(score)
movies = movies.sort_values(by='numVotes',ascending=False)
movies['popularity'] = popularity
movies = movies.drop('isAdult', 1)
movies = movies.drop('tconst', 1)
movies = movies.drop('originalTitle', 1)
movies = movies.drop('titleType', 1)
movies = movies.drop('runtimeMinutes', 1)
movies = movies.drop('endYear', 1)
movies = movies.drop('numVotes', 1)
movies.to_csv('movies.tsv', sep='\t',index=False)