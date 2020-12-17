import pandas as pd
import random

movie_db = pd.read_csv('movie_finder/movies.tsv', sep='\t', low_memory=False)


class Recommender:
    """
    Representation of a movie recommendation generator.

    Attributes:
        _current_movies: An empty list that will store the movies that will
        be recommended.
        _state: A string representing if the recommender is currently asking
        for a genre or searching for movies.
        _search_db: An dataframe that represents the database of movies that
        fulfill the user parameters.
    """
    def __init__(self):
        """
        Create a new Recommender instance.
        """
        self._current_movies = []
        self._search_db = None

    def reset(self):
        """
        Reset the initial variables to their default values to restart the
        program.
        """
        self._current_movies = []
        self._search_db = None

    def create_search_database(self, popularity, rating, low_year, high_year,
                               genre):
        """
        Create a smaller database of valid movies based on given parameters.

        Args:
            popularity: An integer representing the popularity of the movie.
            low_year: An integer representing the oldest year a movie should be
            from.
            high_year: An integer representing the most recent year a movie
            should be from.
            rating: A float representing the user rating of the movie.
        """
        search_db = movie_db
        search_db = search_db[search_db['popularity'] >= popularity]
        if rating is not None:
            search_db = search_db[search_db['averageRating'] >= rating]
        if low_year is not None:
            search_db = search_db[search_db['startYear'] >= low_year]
        if high_year is not None:
            search_db = search_db[search_db['startYear'] <= high_year]
        if genre is not None:
            search_db = search_db[search_db.genres.str.contains(genre)]
        self._search_db = search_db
        return search_db

    def find_movies(self):
        """
        Randomly select up to 5 movies from the database.

        Returns:
            A list of up to 5 movies, their release year and their user rating.
        """
        num_movies = len(self._search_db)
        if num_movies == 0:
            print('No more movies were found based on your criteria.')
            return None
        movie_list = []
        movie_ids = []
        if num_movies < 5:
            for _ in range(num_movies):
                movie_title = self._search_db.iloc[0]['primaryTitle']
                movie_year = self._search_db.iloc[0]['startYear']
                movie_rating = self._search_db.iloc[0]['averageRating']
                movie = (movie_title + ' (' + str(movie_year) + ')' + ' '
                         + str(movie_rating))
                movie_list.append(movie)
                self._search_db = self._search_db.drop(
                    self._search_db.index[0], 0)
            return movie_list
        movies_to_get = []
        for _ in range(5):
            movie_number = random.randrange(0, num_movies, 1)
            while movie_number in movies_to_get:
                movie_number = random.randrange(0, num_movies, 1)
            movies_to_get.append(movie_number)
        for i in range(5):
            movie_title = (self._search_db.iloc[movies_to_get[i]]
                           ['primaryTitle'])
            movie_year = self._search_db.iloc[movies_to_get[i]]['startYear']
            movie_rating = (self._search_db.iloc[movies_to_get[i]]
                            ['averageRating'])
            movie_id = self._search_db.index[movies_to_get[i]]
            movie = (movie_title + ' (' + str(movie_year) + ')' + ' '
                     + str(movie_rating))
            movie_list.append(movie)
            movie_ids.append(movie_id)
        for i in range(5):
            self._search_db = self._search_db.drop(index=movie_ids[i])
        self._current_movies = movie_list
        return movie_list


class View:
    """
    View for movie recommender.

    Attributes:
        genres: A list of movie genres.
    """
    genres = ['Romance', 'Drama', 'Comedy', 'Crime', 'War', 'Sci-Fi',
              'Western', 'Adventure', 'Documentary', 'Biography', 'Action',
              'Horror', 'Fantasy', 'Mystery', 'History', 'Animation',
              'Musical', 'Thriller', 'Family', 'Music', 'Sport', 'Film-Noir']

    def show_genres(self):
        """
        Print the available genres to search within.
        """
        for i in range(len(self.genres)):
            print(self.genres[i])

    def show_movies(self, movies):
        """
        Print the recommended movies.

        Args:
            movies: A list of movies to print.
        """
        if movies is not None:
            for i in range(len(movies)):
                print(movies[i])


class Controller:
    """
    Controller for movie recommender.
    """
    genres = ['Romance', 'Drama', 'Comedy', 'Crime', 'War', 'Sci-Fi',
              'Western', 'Adventure', 'Documentary', 'Biography', 'Action',
              'Horror', 'Fantasy', 'Mystery', 'History', 'Animation',
              'Musical', 'Thriller', 'Family', 'Music', 'Sport', 'Film-Noir']

    def ask_for_year(self):
        """
        Ask the user if the search should be limited by year. If yes, ask for
        a low year and high year to bracket the search.

        Returns:
            A list of length 2 containing the low year and high year or None
            and None if the user does not want to limit the search by year.
        """
        low_year = 2020.1
        high_year = 2020.1
        yesno = input(
            "Do you want to search movies by year? (Enter yes or no): ")
        while yesno != 'yes' and yesno != 'no':
            yesno = input('Invalid input, please enter yes or no. ')
        if yesno == 'no':
            return [None, None]
        while low_year > 2020 or low_year < 0:
            if low_year != 2020.1:
                print("Please enter a valid year.")
            while True:
                try:
                    low_year = int(input(
                        'How far back do you want to search for movies? '
                        '(Enter a year like 1984): '))
                    break
                except:
                    print("Please enter a valid year.")
        while high_year > 2020 or high_year < 0:
            if high_year != 2020.1:
                print("Please enter a valid year.")
            while True:
                try:
                    high_year = int(input('How recent do you want to search'
                                    ' for movies? (Enter a year like 2020): '))
                    break
                except:
                    print("Please enter a valid year.")
        return [low_year, high_year]

    def ask_for_genre(self):
        """
        Ask the user to enter a genre.

        Returns:
            A string representing the selected genre.
        """
        while True:
            genre = input("Enter which genre you would like to watch: ")
            for i in range(len(self.genres)):
                if genre == self.genres[i]:
                    return genre
            print('Invalid genre.')

    def ask_for_rating(self):
        """
        Ask the user if they want to limit the search by rating. If yes, ask
        for a minimum rating.

        Returns:
            An float representing the minimum user rating that should be
            included in the search.
        """
        yesno = input("Do you want to limit your search by rating?"
                      " (Enter yes or no): ")
        while yesno != 'yes' and yesno != 'no':
            yesno = input('Invalid input, please enter yes or no. ')
        if yesno == 'no':
            return None
        rating = 11.173
        while rating > 10 or rating < 0:
            if rating != 11.173:
                print("Please enter a valid rating.")
            while True:
                try:
                    rating = float(input('Enter a minimum rating from 0-10.'
                                   ' (ex. 7.5): '))
                    break
                except:
                    print("Please enter a valid rating.")
        return rating

    def ask_for_instruction(self):
        """
        Ask the user if the program should search again or reset.

        Returns:
            Return a string signifying an instruction to be followed.
        """
        instruction = input(
            "Type search to search again or reset to reset the parameters: ")
        if instruction != 'search' and instruction != 'reset':
            while instruction != 'search' and instruction != 'reset':
                print("Invalid input")
                instruction = input(
                    "Type search to search again or reset to reset the"
                    " parameters: ")
        return instruction

    def ask_for_expansion(self):
        """
        Ask the user if less popular movies should be included.

        By default the search only includes the 10% most popular movies, this
        function asks the user if this should be expanded in increments of 10%.

        Returns:
            An integer representing the worst popularity value that should be
            included in the search.
        """
        expand = 'yes'
        popularity = 10
        print('By default the search only includes the top 10% most popular'
              ' movies.')
        yesno = input("Would you like to expand the search to include more"
                      " movies? (Enter yes or no): ")
        while yesno != 'yes' and yesno != 'no':
            yesno = input('Invalid input, please enter yes or no. ')
        if yesno == 'no':
            return popularity
        popularity -= 1
        while expand == 'yes':
            percentage = 110 - popularity * 10
            print('The search will now include the top ', percentage,
                  '% most popular movies.', sep='')
            expand = input("Would you like to expand the search further?: ")
            while expand != 'yes' and expand != 'no':
                expand = input('Invalid input, please enter yes or no. ')
            popularity -= 1
            if popularity == 1:
                print('The search will now include all movies.')
                expand = 'no'
        return popularity


def main():
    """
    Run the movie recommender.
    """
    system = Recommender()
    view = View()
    controller = Controller()

    while True:
        view.show_genres()
        genre = controller.ask_for_genre()
        years = controller.ask_for_year()
        rating = controller.ask_for_rating()
        popularity = controller.ask_for_expansion()
        system.create_search_database(popularity, rating, years[0], years[1],
                                      genre)
        while True:
            movies = system.find_movies()
            view.show_movies(movies)
            instruction = controller.ask_for_instruction()
            if instruction == 'reset':
                system.reset()
                break


if __name__ == "__main__":
    main()
