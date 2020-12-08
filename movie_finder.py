import database as db
import pandas as pd
import random

class Recommender:
    """
    Representation of a movie recommendation generator.

    Attributes:
        _used_movies: An empty list that will store all movies that have
        already been recommended. 
        _current_movies: An empty list that will store the movies that will
        be recommended.
        _state: A string representing if the recommender is currently asking
        for a genre or searching for movies. 
        _limit: An integer representing how many movies should be used in the
        recommendation search. 
    """
    def __init__(self):
        """
        Create a new Recommender instance. 
        """
        self._used_movies = []
        self._current_movies = []
        self._state = "genres"
        self._limit = 50

    def reset(self):
        """
        Reset the initial variables to their default values to restart the
        program.
        """
        self._used_movies = []
        self._current_movies = []
        self._state = "genres"
        self._limit = 50

    def find_movies(self, genre):
        """
        Randomly select 8 movies that are within the given genre.

        Args:
            genre: A string representing the genre to search from.
        """
        genre_movies = db.movies[db.movies.genres.str.contains(genre)]
        num_movies = len(genre_movies)
        movies_to_get = []
        for i in range(5):
            movie_number = random.randrange(0, num_movies, 1)
            movies_to_get.append(movie_number)
        movie_list = []
        for i in range(5):
            movie_title = genre_movies.iloc[movies_to_get[i]]['primaryTitle']
            movie_list.append(movie_title)
        self._current_movies = movie_list

    def expand_search(self):
        """
        Expand the pool of movies to search from by 50.
        """
        self._limit += 50
        print("Search has been expanded.")

    def search(self):
        """
        Signify that the program is searching movies.
        """
        self._state = "searching"

    def get_movies(self):
        """
        Return the current movies to be recommended.
        """
        return self._current_movies

    def get_state(self):
        """
        Return the current state of the program.
        """
        return self._state

    def ended(self):
        """
        End the program.
        """
        pass


class View:
    """
    View for movie recommender.

    Attributes:
        genres: A list of movie genres.
        _system: A recommender instance.
    """
    genres = ['Action', 'Crime', 'Drama']

    def __init__(self, system):
        """
        Create View for movie recommender.

        Args:
            system: A Recommender instance.
        """
        self._system = system

    def show_genres(self):
        """
        Print the available genres to search within.
        """
        for i in range(len(self.genres)):
            print(self.genres[i])

    def show_movies(self):
        """
        Print the recommended movies.
        """
        movies = self._system.get_movies()
        for i in range(len(movies)):
            print(movies[i])


class Controller:
    """
    Controller for movie recommender.
    """
    def ask_for_genre(self):
        """
        Ask the user to enter a genre. Return the genre selected by the user.
        """
        genre = input("Enter which genre you would like to watch: ")
        print("You chose:", genre)
        return genre

    def ask_for_instruction(self):
        """
        Ask the user what should be done next. Return a number signifying an
        instruction to be followed.
        """
        instruction = input(
            "Type 1 to search, 2 to expand the search, and 3 to choose a different genre: ")
        if instruction != 1 and instruction != 2 and instruction != 3:
            while instruction != 1 and instruction != 2 and instruction != 3:
                print("Invalid input")
                instruction = input(
                    "Type 1 to search, 2 to expand the search, and 3 to choose a different genre: ")
        return instruction


def main():
    """
    Run the movie recommender.
    """
    system = Recommender()
    view = View(system)
    controller = Controller()

    while not system.ended():
        view.show_genres()
        genre = controller.ask_for_genre()
        system.search()
        while system.get_state() == "searching":
            system.find_movies(genre)
            view.show_movies
            instruction = controller.ask_for_instruction()
            if instruction == 2:
                while instruction == 2:
                    system.expand_search()
                    instruction = controller.ask_for_instruction()
            elif instruction == 3:
                system.reset()


if __name__ == "__main__":
    main()