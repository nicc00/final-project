import pandas as pd
import pytest
import numpy as np
from movie_finder import movie_finder
movie_db = pd.read_csv('movie_finder/movies.tsv', sep='\t', low_memory=False)
test_case_1 = movie_db[movie_db['popularity'] >= 8]
test_case_1 = test_case_1[test_case_1['averageRating'] >= 7.5]
test_case_1 = test_case_1[test_case_1['startYear'] >= 1970]
test_case_1 = test_case_1[test_case_1['startYear'] <= 1980]
test_case_1 = test_case_1[test_case_1.genres.str.contains('Thriller')]
test_case_2 = movie_db[movie_db['popularity'] >= 10]
test_case_2 = test_case_2[test_case_2['startYear'] >= 1970]
test_case_2 = test_case_2[test_case_2['startYear'] <= 1970]
test_case_2 = test_case_2[test_case_2.genres.str.contains('Romance')]
test_case_3 = movie_db[movie_db['popularity'] >= 10]
test_case_3 = test_case_3[test_case_3.genres.str.contains('Action')]
test_case_4 = movie_db[movie_db['popularity'] >= 9]
test_case_4 = test_case_4[test_case_4['averageRating'] >= 8]
test_case_4 = test_case_4[test_case_4.genres.str.contains('Drama')]
test_case_5 = movie_db[movie_db['popularity'] >= 1]
test_case_5 = test_case_5[test_case_5['startYear'] >= 1970]
test_case_5 = test_case_5[test_case_5['startYear'] <= 2020]
test_case_5 = test_case_5[test_case_5.genres.str.contains('Comedy')]


search_db_case = [(8, 7.5, 1970, 1980, 'Thriller', test_case_1),
                  (10, None, 1970, 1970, 'Romance', test_case_2),
                  (10, None, None, None, 'Action', test_case_3),
                  (9, 8, None, None, 'Drama', test_case_4),
                  (1, None, 1970, 2020, 'Comedy', test_case_5)]


@pytest.mark.parametrize('popularity, rating, low_year, high_year, genre,'
                         'test_case', search_db_case)
def test_search_db(popularity, rating, low_year, high_year, genre, test_case):
    system = movie_finder.Recommender()
    assert np.all(system.create_search_database(popularity, rating, low_year,
                  high_year, genre)) == np.all(test_case)
