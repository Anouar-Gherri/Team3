# The Algorithm class


# An Algorithm takes the following input:
# - name (string):
#           A dummy name, e.g. 'RelativeFrequencyAlgorithm'
# - training_function (library-filename crawler_data_file *args -> library-file):
#           a function which takes the Crawler data and trains a
#           'Library file'. The calculations for the probabilities will later
#           base on this file. It also has to return a set of the unique teams.
# - request_function (library-file match-dict -> probability-dict):
#           will calculate the probability based on the library-file and the match specified
#           in the match-dict. The calculated probabilities will be returned as a list
#           with chances for winning, loosing or drawing, referring to the host.
#           e.g. {"host": "munich", "guest": 'dusseldorf', "Place": "munich",
#                 "date": "2009-08-07T20:30:00"}
#                -> [0.4, 0.4, 0.2]
# - data format (string):
#           the format of the trainings data. has to fit with the trainings function.
#           All '.' in the string will be deleted
# - library format (string):
#           the format of the library. has to fit the trainings function an request function.
#           All '.' in the string will be deleted
# - library_name [optional] (str):
#           A name to determine the name of the library file. Case not given,
#           <name> wil be taken.

class Algorithm:
    def __init__(self, name: str, training_function, request_function, data_format: str,
                 library_format: str, library_name: str = ''):
        """Creates a new algorithm.

        :param name: A name for the Algorithm.
        :param training_function: A function using the crawler data to create a 'library'.
               It has to return the set of the unique teams
        :param request_function: A function using the library and match information
               to predict its outcomes
        :param data_format: The file type of the crawler data
        :param library_format: The file type of the library
        :param library_name: An optional input to generate Library files with unique names.
               Case not given, Library_<name> will be used for this.
               Eg: library_name: 'Library_RFA' -> library_filename: Library_RFA.<library_format>

        :type name: str
        :type training_function: function
        :type request_function: function
        :type data_format: str
        :type library_format: str
        :type library_name: str

        :rtype: object (Algorithm)
        """
        self.name = name
        self.training_function = training_function
        self.request_function = request_function

        data_format = data_format.replace('.', '')
        library_format = library_format.replace('.', '')
        library_name = self.name if library_name == '' else library_name

        self.file_types = dict(crawler=data_format, library=library_format)
        self.library_filename = 'Library_{}.{}'.format(library_name, library_format)
        self.trained = False
        self.teams = set()

    # --- Set Properties ---
    def set_name(self, name: str):
        self.name = name

    def set_training_function(self, training_function):
        self.training_function = training_function

    def set_request_function(self, request_function):
        self.request_function = request_function

    def set_file_types(self, file_types: dict):
        self.file_types = file_types

    def set_library_filename(self, library_filename: str):
        self.library_filename = library_filename

    def set_trained(self, trained: bool):
        self.trained = trained

    def set_teams(self, teams: set):
        self.teams = teams

    # --- Common Functions ---
    # Trains the Library (sets obj.trained = true)
    def train(self, crawler_data_file_name, *args):
        """Trains the algorithm. The function will use a file called
        crawler_crawler_data_file_name to create a library called self.library_name.
        Sets the teams attribute.

        :param crawler_data_file_name: The name of the data-file used to create the library
        :param args: additional arguments the training_function may use

        :type crawler_data_file_name: str
        """
        data_format = self.file_types['crawler']
        # Generate the name of the Library from the Algorithm name and Library ending
        if not crawler_data_file_name.endswith(data_format):
            raise ValueError(
                "The type of the requested crawler-data-file does not match the expected type :" + data_format)

        with open(crawler_data_file_name, "r") as data:
            teams = self.training_function(self.library_filename, data, *args)
        data.close()

        self.trained = True
        self.teams = teams

    # Requests a match
    # Output type: {'host': '---', 'win': --%, 'lose': --%, 'draw': --%}
    def request(self, match_dict):
        """Requests match outcomes from the Algorithm by using the library.
        The algorithm has to be trained first!

        :param match_dict: A dictionary specifying the match. The information
        you'll need to specify depends on the information the request_function needs
        :type match_dict: dict

        :return: a dictionary containing the host and his chances of winning, loosing or drawing
        """
        host = match_dict['host']
        guest = match_dict['guest']

        if not self.trained:
            raise NameError('The library "{}" has to be trained first (Use self.train)'.format(self.library_filename))
        # TODO: teams cannot handle ä, ö, ü and maybe other not aswell
        #
        if host not in self.teams:
            raise ValueError("\"{}\" is not in the listed teams!".format(host))
        if guest not in self.teams:
            raise ValueError("\"{}\" is not in the listed teams!".format(guest))

        with open(self.library_filename, "r") as lib:
            results = self.request_function(lib, match_dict)
        lib.close()

        result_dict = results_to_dict(host, results)
        return result_dict


# Helper functions
def results_to_dict(host, results):
    if not len(results) == 3:
        raise ValueError('Result list has to contain 3 entries')
    # Every entry has to be a positive number
    if not all(map(lambda x: isinstance(x, (int, float)) and x >= 0, results)):
        raise ValueError('Result list is not numeric')
    if not sum(results) == 1:
        raise ValueError('Result list is not normalized')

    res_dict = {'host': host}
    res_dict.update({case: res for case, res in zip(["win", "lose", "draw"], results)})
    return res_dict
