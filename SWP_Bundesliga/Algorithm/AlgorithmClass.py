# Probleme:
# - Ist die Struktur gut?
# - Ich bin kein Python Experte- kann man das so machen?
# - Passen die Error-Typen?

# The Algorithm class
class Algorithm:
    def __init__(self, name: str, training_function: function, request_function: function,
                 data_filetype: str, library_filetype: str, library_name: str ='',
                 trained_lib: bool = False):
        # A dummy name, e.g. 'RelativeFrequenzyAlgorithm"
        self.name = name
        # tf : (library-file-name crawler-file -> library_file)
        # Eats a library name and a crawler-data-file and creates a
        # library file with library-file-name
        self.training_function = training_function
        # The filename for the library which somehow stores the probablities
        # e.g. "Library.csv"
        self.library_name = library_name
        # Tells you whether the lib is already trained (created) or not
        self.trained_lib = trained_lib
        # rf : (match-dict library -> probability-dict)
        # Takes a dicionary with match data and returns outcome probabilities
        # e.g. {"host": "munich", "guest": 'dusseldorf', "Place": "munich",
        #      "date": "2009-08-07T20:30:00"}
        #      -> {"win": 0.4, "lose": 0.4, "draw": 0.2} (refering to host)
        self.request_function = request_function
        # A small dictionary stating the file-type of the crawler data and
        # library (e.g. {"crawler": ".csv", "library": ".csv"}
        # The trainings and request functions need to be based on those types
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
    # It will also set obj.library_name to lib_name and obj.trained_lib = true
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
        self.trained_lib = True

    # Requests a match
    # Output type: {"win": --%, "lose": --%, "draw": --%} (refering to host)
    def request(self, match_dict):
        if not self.trained_lib:
            raise NameError('The library "' + self.library_name
                            + '" has to be trained first')

        with open(self.library_name, "r") as lib:
            return self.request_function(match_dict, lib)

