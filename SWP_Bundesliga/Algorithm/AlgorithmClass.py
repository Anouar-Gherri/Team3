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
                 library_format: str, nickname: str = '', train_specifications=None,
                 request_specifications=None):
        """Creates a new algorithm.

        :param name: A name for the Algorithm.
        :param training_function: A function using the crawler data to create a 'library'.
               It has to return the set of the unique teams
        :param request_function: A function using the library and match information
               to predict its outcomes
        :param data_format: The file type of the crawler data
        :param library_format: The file type of the library
        :param nickname: An optional shorter name. Case not given, <name> will be used for this.
               The final form will be Library_<library_name>.<library_format>
        :param train_specifications: A dict specifying settings in the training_function
        :param request_specifications: A dict specifying settings in the training_function


        :type name: str
        :type training_function: function
        :type request_function: function
        :type data_format: str
        :type library_format: str
        :type nickname: str

        :rtype: object (Algorithm)
        """
        if train_specifications is None:
            train_specifications = {}
        if request_specifications is None:
            request_specifications = {}

        data_format = data_format.replace('.', '')
        library_format = library_format.replace('.', '')
        nickname = self.name if nickname == '' else nickname

        self.name = name
        self.training_function = training_function
        self.request_function = request_function
        self.file_types = dict(crawler=data_format, library=library_format)
        self.library_filename = 'Library_{}.{}'.format(nickname, library_format)
        self.trained = False
        self.specifications = dict(train_kwargs=train_specifications, request_kwargs=request_specifications)

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

    def set_train_specifications(self, specifications: dict):
        self.specifications['train_kwargs'] = specifications

    def set_request_specifications(self, specifications: dict):
        self.specifications['request_kwargs'] = specifications

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
                "The type of the requested crawler-data-file does not match the expected type: " + data_format)

        kwargs = self.specifications['train_kwargs']

        with open(crawler_data_file_name, "r") as data:
            self.training_function(self.library_filename, data, *args, **kwargs)
        data.close()

        self.trained = True

    # Requests a match
    # Output type: {'host': '---', 'win': --%, 'lose': --%, 'draw': --%}
    def request(self, match_dict, *args):
        """Requests match outcomes from the Algorithm by using the library.
        The algorithm has to be trained first!

        :param match_dict: A dictionary specifying the match. The information
        you'll need to specify depends on the information the request_function needs
        :type match_dict: dict

        :return: a dictionary containing the host and his chances of winning, loosing or drawing
        """

        if not self.trained:
            raise NameError('The library "{}" has to be trained first (Use self.train)'.format(self.library_filename))

        kwargs = self.specifications['request_kwargs']

        with open(self.library_filename, "r") as lib:
            results = self.request_function(lib, match_dict, *args, **kwargs)
        lib.close()

        host = match_dict['host']
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
