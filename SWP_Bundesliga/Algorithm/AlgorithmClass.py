# Probleme:
# - Ist die Struktur gut?
# - Ich bin kein Python Experte- kann man das so machen?
# - Passen die Error-Typen?


# The Algorithm class
# An Algorithm has the following properties:
# - name (string):
#           a dummy name, e.g. 'RelativeFrequenzyAlgorithm"
# - training_function (library-file-name crawler-file -> library-file):
#           a function wich takes the Crawler data and a library-name and trains a
#           'Libraryfile' with given name. The calculations for the probabilities will later
#           base on this file
# - library_name (string):
#           the filename of the library
# - trained (boolean):
#           tells you whether the algorithm has trained or not
#           (i.e. whether the library exists)
# - request_function (match-dict library-file -> probability-dict):
#           will calculate the probability based on the library-file and the match specified
#           in the match-dict. The calculated probabilites will be returned as a dictionary
#           with chances for winning, loosing or drawing, refering to the host.
#           e.g. {"host": "munich", "guest": 'dusseldorf', "Place": "munich",
#                 "date": "2009-08-07T20:30:00"}
#                -> {'host': 'Munich', 'win': 0.4, 'lose': 0.4, 'draw': 0.2}
# - file_type(dictionary):
#           A small dictionary containing the file-types of the crawler-data and the library.
#           You cannot train unless your crawler-data-file and libname are/have the according
#           filetype
class Algorithm:
    def __init__(self, name: str, training_function, request_function, data_filetype: str,
                 library_filetype: str, library_name: str ='', trained: bool = False):
        self.name = name
        self.training_function = training_function
        self.library_name = library_name
        self.trained = trained
        self.request_function = request_function
        self.file_types = dict(crawler= data_filetype, library=library_filetype)

    # --- Set Properties ---
    def set_name(self, name):
        self.name = name

    def set_training_function(self, training_function):
        self.training_function = training_function

    def set_library(self, library_name):
        self.library_name = library_name

    def set_trained(self, trained):
        self.trained = trained

    def set_request_function(self, request_function):
        self.request_function = request_function

    def set_file_types(self, file_types):
        self.file_types = file_types

    # --- Common Funcitons ---
    # Trains the Library
    # It will also set obj.library_name to lib_name and obj.trained = true
    def train(self, lib_name, crawler_data_file_name):
        if not crawler_data_file_name.endswith(self.file_types["crawler"]):
            raise ValueError(
                "The type of the requested crawler-data-file does not match"
                "the expected type :" + self.file_types["crawler"])

        if not lib_name.endswith(self.file_types["library"]):
            raise ValueError(
                "The type of the library name does not match"
                "the expected type :" + self.file_types["crawler"])

        with open(crawler_data_file_name, "r") as data:
            self.training_function(lib_name, data)
        data.close()

        self.library_name = lib_name
        self.trained = True

    # Requests a match
    # Output type: {'host': '---', 'win': --%, 'lose': --%, 'draw': --%}
    def request(self, match_dict):
        if not self.trained:
            raise NameError('The library "' + self.library_name
                            + '" has to be trained first')

        with open(self.library_name, "r") as lib:
            return self.request_function(match_dict, lib)

