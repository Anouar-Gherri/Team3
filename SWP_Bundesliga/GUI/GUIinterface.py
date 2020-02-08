#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from _datetime import datetime
import csv
from Crawler import crawler_class
from builtins import int
from texttable import Texttable
from GUI.current_games import TheCurrentLists
from Algorithm import algorithm_dict, algorithm3
import numpy
import urllib.request


class GUI:
    def __init__(self):
        """Builds the main window of the GUI."""
        # window properties
        self.root = Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.state('zoomed')
        self.root.title('Bundesliga Vorhersage')
        # structural attributes
        self.main_grid = Frame(self.root)
        self.main_grid.pack()

        self.frame_config = Frame(self.main_grid)
        self.frame_current = Frame(self.main_grid)
        self.frame_teamselection = Frame(self.main_grid)
        self.frame_prediction = Frame(self.main_grid)
        self.frame_NMD = Frame(self.main_grid)
        self.spacing = 10

        # load all gui objects
        self.init_crawler_objects()
        self.init_training_objects()
        self.init_team_selection_objects()
        self.init_prediction_objects()
        # next matchday table
        self.init_NMD_table()
        # position all objects
        self.frame_config.grid(row=0)
        self.frame_current.grid(row=1)
        self.frame_teamselection.grid(row=2)
        self.frame_prediction.grid(row=3)
        self.frame_NMD.grid(row=4)

    def init_crawler_objects(self):
        """Builds the GUI objects pertaining to the crawler."""
        self.list_leagues = {'1. Bundesliga': 'bl1',
                             '2. Bundesliga': 'bl2',
                             '3. Bundesliga': 'bl3', }
        leagues = [x for x in self.list_leagues.keys()]

        self.label_league = Label(self.frame_config, text='League: ')
        self.select_league = ttk.Combobox(
            self.frame_config,
            values=leagues,
            width=cbb_width(
                leagues),
            state='readonly')
        self.select_league.current(0)
        self.select_league.bind('<<ComboboxSelected>>', self.update_SMD)

        self.label_crawl_from = Label(self.frame_config, text='From:')
        self.select_crawl_from_season = ttk.Combobox(
            self.frame_config,
            values=[],
            width=cbb_width([]))
        self.select_crawl_from_md = ttk.Combobox(
            self.frame_config,
            width=cbb_width([]))

        self.label_crawl_to = Label(self.frame_config, text='To:')
        self.select_crawl_to_season = ttk.Combobox(
            self.frame_config,
            values=[],
            width=cbb_width([]))
        self.select_crawl_to_md = ttk.Combobox(
            self.frame_config,
            width=cbb_width([]))
        self.button_crawler = Button(self.frame_config,
                                     text='Start Crawler',
                                     command=self.start_crawler)
        self.status_crawled = Label(self.frame_config, text='')

        self.label_league.grid(row=0, column=0)
        self.select_league.grid(row=0, column=1)
        self.frame_config.grid_columnconfigure(2, minsize=self.spacing)
        self.label_crawl_from.grid(row=0, column=3)
        self.select_crawl_from_season.grid(row=0, column=4)
        self.select_crawl_from_md.grid(row=0, column=5)
        self.frame_config.grid_columnconfigure(6, weight=1)
        self.label_crawl_to.grid(row=0, column=7)
        self.select_crawl_to_season.grid(row=0, column=8)
        self.select_crawl_to_md.grid(row=0, column=9)
        self.frame_config.grid_columnconfigure(10, minsize=self.spacing)
        self.button_crawler.grid(row=0, column=11, sticky=N + S + E + W)
        self.status_crawled.grid(row=0, column=12)
        self.frame_config.grid_columnconfigure(12, minsize=50)

        # display: current state
        self.label_current_dataset = Label(self.frame_current, text='')
        self.label_current_dataset.grid(row=0)

    def init_training_objects(self):
        """Builds the GUI objects pertaining to the training."""
        self.dict_algorithm = algorithm_dict.create_algorithms()
        self.list_algorithms = [name for name in self.dict_algorithm.keys()]
        self.list_algorithms.insert(0, 'Train all')
        self.is_trained = []
        for algo in range(len(self.list_algorithms) - 1):
            self.is_trained.append(None)

        self.frame_algorithm = Frame(self.frame_config)
        self.label_algorithm = Label(
            self.frame_algorithm,
            text='Select algorithm:')
        self.select_algorithm = ttk.Combobox(
            self.frame_algorithm,
            values=self.list_algorithms,
            width=cbb_width(
                self.list_algorithms),
            state='readonly')
        self.select_algorithm.current(0)
        self.update_SMD(None)
        self.button_training = Button(self.frame_config,
                                      text='Start Training',
                                      command=self.start_training,
                                      state='disabled')
        self.status_training = Label(self.frame_config, text='')

        self.frame_algorithm.grid(row=1, column=3, columnspan=7)
        self.label_algorithm.grid(row=0, column=0)
        self.select_algorithm.grid(row=0, column=1)
        self.button_training.grid(row=1, column=11)
        self.status_training.grid(row=1, column=12)

        # display: current state
        self.label_current_algorithm = Label(self.frame_current, text='')
        self.label_current_algorithm.grid(row=1)

    def init_team_selection_objects(self):
        """Builds the GUI objects pertaining to the team selection."""
        self.label_hometeam = Label(
            self.frame_teamselection,
            text='Home Team:')
        self.select_home = ttk.Combobox(
            self.frame_teamselection, width=2, state='readonly')
        self.select_home_current = self.select_home.current()
        self.select_home.bind('<<ComboboxSelected>>', self.update_selection)
        self.label_awayteam = Label(
            self.frame_teamselection,
            text='Away Team:')
        self.select_away = ttk.Combobox(
            self.frame_teamselection, width=2, state='readonly')
        self.select_away_current = self.select_away.current()
        self.select_away.bind('<<ComboboxSelected>>', self.update_selection)
        self.label_hometeam.grid(row=0, column=0)
        self.select_home.grid(row=0, column=1)
        self.label_awayteam.grid(row=1, column=0)
        self.select_away.grid(row=1, column=1)

    def init_prediction_objects(self):
        """Builds the GUI objects pertaining to the match prediction."""
        self.button_prediction = Button(self.frame_prediction,
                                        text='Start Prediction',
                                        command=self.start_prediction,
                                        state='disabled')
        self.status_prediction = Label(self.frame_prediction, text='\n\n')
        self.frame_result_table = Frame(self.frame_prediction)

        self.button_prediction.grid(row=0)
        self.status_prediction.grid(row=1)
        self.frame_result_table.grid(row=2)
        Label(self.frame_prediction, text='').grid(row=3)

    def init_NMD_table(self):
        year = get_current_season("bl1")
        next_game_list = TheCurrentLists(year)
        list_of_the_next_games = next_game_list.GetTheListOfTheNextRoundIfItExist[0]
        list_of_the_next_games_to_be_predicted = next_game_list.GetTheListOfTheNextRoundIfItExist[1]
        rouund = next_game_list.GetTheListOfTheNextRoundIfItExist[2]
        list_length = len(list_of_the_next_games)
        #hier sollte ein Poisson regression deklariert und trainiert
        #####
        self.dict_algorithm.get('PoissonAlgorithm').train('matches.csv')
        #####
        t = Texttable(0)
        t.set_chars(['', '', '', ''])
        t.set_deco(Texttable.BORDER | Texttable.HEADER |
                   Texttable.HLINES | Texttable.VLINES)
        t.header(["Next Matches will be:"])
        t.set_cols_align(["c"])
        list1 = []
        if list_length == 1:
            t.add_row(list_of_the_next_games[0])
        else:
            for i in range(list_length):
                match_request = dict(
                    host=list_of_the_next_games_to_be_predicted[i][0],
                    guest=list_of_the_next_games_to_be_predicted[i][0])
                #hier wurde der algorithm benutzt um einzelne ergebnisse zu liefern
               #####
                result=self.dict_algorithm[0].request(match_request)
               ######
                texte = '  HomeTeam: ' + "{:.2%}  ".format(result.get('win')) + '  AwayTeam: ' + "{:.2%}  ".format(
                    result.get('lose')) + '  Draw: ' + "{:.2%}  ".format(result.get('draw'))
                list1.append(texte)
            lengthlist1 = len(list1)
            list1 = numpy.array(numpy.resize(list1, (lengthlist1, 1)))
            print(list1)
            if (lengthlist1 == list_length):
                for i in range(list_length):
                    print(list_of_the_next_games[i][0])
                    print(list_of_the_next_games)
                    t.add_row(list_of_the_next_games[i])
                    t.add_row(list1[i])
        table = Label(self.frame_NMD, text=t.draw(), relief=GROOVE)

        # Vertical (y) Scroll Bar
        yscrollbar = Scrollbar(self.frame_NMD)
        yscrollbar.pack(side=LEFT, expand=TRUE,fill=Y)
        # Text Widget
        text = Text(self.frame_NMD, yscrollcommand=yscrollbar.set)
        text.tag_configure("center", justify='center')
        text.insert("1.0", table['text'])
        text.tag_add("center", "1.0", "end")
        text.pack(fill="both", expand=True)
        text.config(
            state=DISABLED,
            width=110,
            height=25,
            bg='green',
            fg="white",
            font='helvetica 12')


    def init_list_teams(self):
        """Sets team selection options based on crawled data."""
        self.list_teamselection = []
        with open('teams.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for team in reader:
                if team['name'] not in self.list_teamselection:
                    self.list_teamselection.append(team['name'])
        self.list_teamselection.sort()
        self.select_home.config(values=self.list_teamselection,
                                width=cbb_width(self.list_teamselection))
        self.select_away.config(values=self.list_teamselection,
                                width=cbb_width(self.list_teamselection))

    def start_crawler(self):
        """Starts the crawler after checking input values and inserting default values."""
        if self.select_league.current() == -1:
            return_invalid(self.status_crawled)
            return
        league = self.list_leagues.get(self.select_league.get())
        this_season = get_current_season(league)
        self.crd_from_season = self.select_crawl_from_season.get()
        self.crd_from_md = self.select_crawl_from_md.get()
        self.crd_to_season = self.select_crawl_to_season.get()
        self.crd_to_md = self.select_crawl_to_md.get()
        self.current_crawl = crawler_class.Crawler(league)
        # if no selection made default to current season
        if self.crd_to_season == '':
            self.crd_to_season = this_season
        elif self.select_crawl_to_season.current() == -1:
            return_invalid(self.status_crawled)
            return
        else:
            self.crd_to_season = int(self.crd_to_season)
        # if no selection made default to selected crd_to_season
        if self.crd_from_season == '':
            self.crd_from_season = self.crd_to_season
        elif self.select_crawl_from_season.current() == -1:
            return_invalid(self.status_crawled)
            return
        else:
            self.crd_from_season = int(self.crd_from_season)
        # if no selection made default to first matchday
        if self.crd_from_md == '':
            self.crd_from_md = 1
        elif self.select_crawl_from_md.current() == -1:
            return_invalid(self.status_crawled)
            return
        else:
            self.crd_from_md = int(self.crd_from_md)
        # if no selection made default to last matchday
        if self.crd_to_md == '':
            self.crd_to_md = self.current_crawl.get_group_size(2018)
        elif self.select_crawl_to_md.current() == -1:
            return_invalid(self.status_crawled)
            return
        else:
            self.crd_to_md = int(self.crd_to_md)
        if (self.crd_from_season > self.crd_to_season
                or (self.crd_from_season == self.crd_to_season
                    and self.crd_from_md > self.crd_to_md)):
            return_invalid(self.status_crawled)
            return
        self.current_crawl.get_match_data_interval(self.crd_from_season,
                                                   self.crd_from_md,
                                                   self.crd_to_season,
                                                   self.crd_to_md)
        self.current_crawl.get_teams(self.crd_from_season, self.crd_to_season)
        self.status_crawled['text'] = 'Done'
        self.label_current_dataset['text'] = "Current data: {}.{}.{}-{}.{}".format(
            league, self.crd_from_season, self.crd_from_md, self.crd_to_season, self.crd_to_md)
        self.button_training['state'] = 'normal'

    def start_training(self):
        """Call selected algorithm."""
        if self.select_algorithm.current() == -1:
            return
        self.current_algorithm = self.select_algorithm.current()
        if self.current_algorithm == 0:
            algorithm_dict.train_all(self.dict_algorithm, 'matches.csv')
        else:
            self.dict_algorithm.get(
                self.select_algorithm.get()).train('matches.csv')


        self.status_training['text'] = 'Done'
        self.label_current_algorithm['text'] = "Current training: {}".format(
            self.select_algorithm.get())
        self.button_prediction['state'] = 'normal'
        self.init_list_teams()

    def start_prediction(self):
        """Retrieves and displays prediction for selected match."""
        home_pick = self.select_home.current()
        away_pick = self.select_away.current()
        if (home_pick == -1 or away_pick == -1):
            return
        match_request = dict(host=self.list_teamselection[home_pick],
                             guest=self.list_teamselection[away_pick])
        Label(
            self.frame_result_table,
            relief=GROOVE,
            text='Algorithm').grid(
            row=0,
            column=0,
            sticky=N + S + E + W)
        Label(
            self.frame_result_table,
            relief=GROOVE,
            text='Win').grid(
            row=0,
            column=1,
            sticky=N + S + E + W)
        Label(
            self.frame_result_table,
            relief=GROOVE,
            text='Lose').grid(
            row=0,
            column=2,
            sticky=N + S + E + W)
        Label(
            self.frame_result_table,
            relief=GROOVE,
            text='Draw').grid(
            row=0,
            column=3,
            sticky=N + S + E + W)
        for a in range(1, len(self.list_algorithms)):
            if self.current_algorithm == 0 or a == self.current_algorithm:
                self.is_trained[a - 1] = self.dict_algorithm[self.list_algorithms[a]
                                                             ].request(match_request)
                print(self.list_algorithms[0])
                name = self.list_algorithms[a]
                win = "{:.2%}".format(self.is_trained[a - 1]['win'])
                lose = "{:.2%}".format(
                    self.is_trained[a - 1]['lose'])
                draw = "{:.2%}".format(
                    self.is_trained[a - 1]['draw'])

                Label(
                    self.frame_result_table,
                    relief=GROOVE,
                    text=name).grid(
                    row=a,
                    column=0,
                    sticky=N + S + E + W)
                Label(
                    self.frame_result_table,
                    relief=GROOVE,
                    text=win).grid(
                    row=a,
                    column=1,
                    sticky=N + S + E + W)
                Label(
                    self.frame_result_table,
                    relief=GROOVE,
                    text=lose).grid(
                    row=a,
                    column=2,
                    sticky=N + S + E + W)
                Label(
                    self.frame_result_table,
                    relief=GROOVE,
                    text=draw).grid(
                    row=a,
                    column=3,
                    sticky=N + S + E + W)
            else:
                for widget in self.frame_result_table.grid_slaves(row=a):
                    widget.destroy()

        status_text = "{}{}{}{}{}".format('\nPrediction for ',
                                          self.list_teamselection[home_pick],
                                          ' (host) against ',
                                          self.list_teamselection[away_pick],
                                          ' is:\n')
        self.status_prediction['text'] = status_text

    def update_selection(self, select):
        """Switches home team and away team selection if the user tries to select the same team twice."""
        if (self.select_home.get() == self.select_away_current):
            self.select_away.set(self.select_home_current)
            self.select_home_current = self.select_home.get()
            self.select_away_current = self.select_away.get()
        elif (self.select_away.get() == self.select_home_current):
            self.select_home.set(self.select_away_current)
            self.select_away_current = self.select_away.get()
            self.select_home_current = self.select_home.get()
        else:
            self.select_home_current = self.select_home.get()
            self.select_away_current = self.select_away.get()

    def update_SMD(self, s):
        """Updates matchday selection according to selected league."""
        league = self.list_leagues.get(self.select_league.get())
        crawler = crawler_class.Crawler(league)
        seasons = get_seasons(league)
        MD = [x for x in range(1, crawler.get_group_size(2018) + 1)]
        self.select_crawl_from_season.config(values=seasons,
                                             width=cbb_width(seasons))
        self.select_crawl_from_season.set(seasons[-2])
        self.select_crawl_to_season.config(values=seasons,
                                           width=cbb_width(seasons))
        self.select_crawl_to_season.set(seasons[-2])
        self.select_crawl_from_md.config(values=MD,
                                         width=cbb_width(MD))
        self.select_crawl_from_md.current(0)
        self.select_crawl_to_md.config(values=MD,
                                       width=cbb_width(MD))
        self.select_crawl_to_md.set(MD[-1])


def get_seasons(league):
    """Returns a list with all the Bundesliga seasons from 2002/2003 to now."""
    current = get_current_season(league)
    first_season = 2008
    all_seasons = []
    for i in range(first_season, current + 1):
        all_seasons.append(i)
    return all_seasons


def is_season_finished(league, year):
    """Checks if all matches in a season have finished"""
    data = {'date': [],
            'team1': [],
            'team2': [],
            'is_finished': [],
            'play_day': [],
            'goal1': [],
            'goal2': []}
    crawler = crawler_class.Crawler(league)
    max_MD = crawler.get_group_size(year)
    last_match = crawler.get_data(year, data, 1, max_MD)
    if (last_match['is_finished'] and all(last_match['is_finished'])):
        return True
    else:
        return False


def get_current_season(league):
    """Return the current season based on current year or last year if season still unfinished"""
    this_year = datetime.today().year
    if is_season_finished(league, this_year - 1):
        return this_year
    else:
        return this_year - 1


# visuals

def return_invalid(status):
    """Displays a text to let the user know that an invalid input has been made."""
    status['text'] = 'Invalid'


def cbb_width(list):
    """Calculates an appropriate size for comboboxes depending on their values."""
    return 1 if not list else max(len(str(x)) for x in list) + 1


def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.request.URLError as err:
        return False


def initiate_gui():
    if internet_on():
        gui_object = GUI()
        gui_object.root.mainloop()
    else:
        return print('NO INTERNET')


if __name__ == '__main__':
    initiate_gui()