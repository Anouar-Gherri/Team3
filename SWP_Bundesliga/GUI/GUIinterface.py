#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from _datetime import datetime
import csv
from Crawler import crawler_class
from builtins import int
from texttable import Texttable
from GUI.current_games import TheCurrentLists
from Algorithm import algorithm_dict


class GUI:
    def __init__(self):
        """Builds the main window of the GUI."""
        # window properties
        self.root = Tk()
        self.root.geometry('1000x1000')
        self.root.state('zoomed')
        self.root.title('Bundesliga Vorhersage')

        # structural attributes
        self.main_grid = Frame(self.root)
        self.main_grid.pack()

        self.frame_config = Frame(self.main_grid)
        self.frame_current = Frame(self.main_grid)
        self.frame_teamselection = Frame(self.main_grid)
        self.frame_NMD = Frame(self.main_grid)

        self.spacing = 10

        # crawler objects
        self.init_crawler_objects()
        # training objects
        self.init_training_objects()

        # team selection objects
        self.init_team_selection_objects()
        # prediction objects
        self.button_prediction = Button(self.main_grid,
                                        text='Start Prediction',
                                        command=self.start_prediction,
                                        state='disabled')
        self.status_prediction = Label(self.main_grid, text='\n\n\n\n')
        # next matchday table
        self.init_NMD_table()
        # position all objects
        self.frame_config.grid(row=0)
        self.frame_current.grid(row=1)
        self.frame_teamselection.grid(row=2)
        self.button_prediction.grid(row=3)
        self.status_prediction.grid(row=4)
        self.frame_NMD.grid(row=5)

    def init_crawler_objects(self):
        """Builds the GUI objects pertaining to the crawler."""
        self.list_seasons = self.get_seasons()
        self.list_matchdays = [x for x in range(1, 35)]

        self.label_crawl_from = Label(self.frame_config, text='From:')
        self.select_crawl_from_season = ttk.Combobox(
            self.frame_config,
            values=self.list_seasons,
            width=self.cbb_width(
                self.list_seasons))
        self.select_crawl_from_md = ttk.Combobox(
            self.frame_config,
            values=self.list_matchdays,
            width=self.cbb_width(
                self.list_matchdays))

        self.label_crawl_to = Label(self.frame_config, text='To:')
        self.select_crawl_to_season = ttk.Combobox(
            self.frame_config,
            values=self.list_seasons,
            width=self.cbb_width(
                self.list_seasons))
        self.select_crawl_to_md = ttk.Combobox(
            self.frame_config,
            values=self.list_matchdays,
            width=self.cbb_width(
                self.list_matchdays))
        self.button_crawler = Button(self.frame_config,
                                     text='Start Crawler',
                                     command=self.start_crawler)
        self.status_crawled = Label(self.frame_config, text='')

        self.label_crawl_from.grid(row=0, column=0)
        self.select_crawl_from_season.grid(row=0, column=1)
        self.select_crawl_from_md.grid(row=0, column=2)
        self.frame_config.grid_columnconfigure(3, weight=1)
        self.label_crawl_to.grid(row=0, column=4)
        self.select_crawl_to_season.grid(row=0, column=5)
        self.select_crawl_to_md.grid(row=0, column=6)
        self.frame_config.grid_columnconfigure(7, minsize=self.spacing)
        self.button_crawler.grid(row=0, column=8, sticky=N + S + E + W)
        self.status_crawled.grid(row=0, column=9)
        self.frame_config.grid_columnconfigure(9, minsize=50)

        # display: current state
        self.label_current_dataset = Label(self.frame_current, text='')
        self.label_current_dataset.grid(row=0)

    def init_training_objects(self):
        """Builds the GUI objects pertaining to the training."""
        self.dict_algorithm = algorithm_dict.create_algorithms()
        self.list_algorithms = [name for name in self.dict_algorithm.keys()]

        self.frame_algorithm = Frame(self.frame_config)
        self.label_algorithm = Label(
            self.frame_algorithm,
            text='Select algorithm:')
        self.select_algorithm = ttk.Combobox(
            self.frame_algorithm,
            values=self.list_algorithms,
            width=self.cbb_width(
                self.list_algorithms),
            state='readonly')
        self.button_training = Button(self.frame_config,
                                      text='Start Training',
                                      command=self.start_training,
                                      state='disabled')
        self.status_training = Label(self.frame_config, text='')

        self.frame_algorithm.grid(row=1, columnspan=7)
        self.label_algorithm.grid(row=0, column=0)
        self.select_algorithm.grid(row=0, column=1)
        self.button_training.grid(row=1, column=8)
        self.status_training.grid(row=1, column=9)

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

    def init_NMD_table(self):
        next_game_list = TheCurrentLists(datetime.today().year)
        list_of_the_next_games = next_game_list.GetTheListOfTheNextRoundIfItExist()
        list_length = len(list_of_the_next_games)
        t = Texttable(0)
        t.set_chars(['', '', '', ''])
        t.set_deco(Texttable.BORDER | Texttable.HEADER |
                   Texttable.HLINES | Texttable.VLINES)
        t.header(["Next Matches will be:"])
        t.set_cols_align(["c"])
        if list_length == 1:
            t.add_row(list_of_the_next_games[0])
        else:
            for i in range(list_length):
                t.add_row(list_of_the_next_games[i])
        table = Label(self.frame_NMD, text=t.draw())
        table.grid(row=0)

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
                                width=self.cbb_width(self.list_teamselection))
        self.select_away.config(values=self.list_teamselection,
                                width=self.cbb_width(self.list_teamselection))

    def start_crawler(self):
        """Starts the crawler after checking input values and inserting default values."""
        this_season = datetime.today().year
        self.crd_from_season = self.select_crawl_from_season.get()
        self.crd_from_md = self.select_crawl_from_md.get()
        self.crd_to_season = self.select_crawl_to_season.get()
        self.crd_to_md = self.select_crawl_to_md.get()
        # if no selection made default to current season
        if self.crd_to_season == '':
            self.crd_to_season = this_season
        elif self.select_crawl_to_season.current() == -1:
            self.return_invalid(self.status_crawled)
            return
        else:
            self.crd_to_season = int(self.crd_to_season)
        # if no selection made default to selected crd_to_season
        if self.crd_from_season == '':
            self.crd_from_season = self.crd_to_season
        elif self.select_crawl_from_season.current() == -1:
            self.return_invalid(self.status_crawled)
            return
        else:
            self.crd_from_season = int(self.crd_from_season)
        # if no selection made default to first matchday
        if self.crd_from_md == '':
            self.crd_from_md = 1
        elif self.select_crawl_from_md.current() == -1:
            self.return_invalid(self.status_crawled)
            return
        else:
            self.crd_from_md = int(self.crd_from_md)
        # if no selection made default to last matchday
        if self.crd_to_md == '':
            self.crd_to_md = 34
        elif self.select_crawl_to_md.current() == -1:
            self.return_invalid(self.status_crawled)
            return
        else:
            self.crd_to_md = int(self.crd_to_md)
        if (self.crd_from_season > self.crd_to_season
                or (self.crd_from_season == self.crd_to_season
                    and self.crd_from_md > self.crd_to_md)):
            self.return_invalid(self.status_crawled)
            return
        self.current_crawl = crawler_class.Crawler(
            "https://www.openligadb.de/api")
        self.current_crawl.get_match_data_interval(self.crd_from_season,
                                                   self.crd_from_md,
                                                   self.crd_to_season,
                                                   self.crd_to_md)
        self.current_crawl.get_teams(self.crd_from_season, self.crd_to_season)
        self.status_crawled['text'] = 'Done'
        self.label_current_dataset['text'] = "Current data: {}.{}-{}.{}".format(
            self.crd_from_season, self.crd_from_md, self.crd_to_season, self.crd_to_md)
        self.button_training['state'] = 'normal'

    def start_training(self):
        """Call selected algorithm."""
        if self.select_algorithm.current() == -1:
            return
        self.current_algorithm = self.dict_algorithm.get(
            self.select_algorithm.get())
        self.current_algorithm.train('matches.csv')

        self.status_training['text'] = 'Done'
        self.label_current_algorithm['text'] = "Current training: {}".format(
            self.select_algorithm.get())
        self.button_prediction['state'] = 'normal'
        self.init_list_teams()

    def start_prediction(self):
        home_pick = self.select_home.current()
        away_pick = self.select_away.current()
        if (home_pick == -1 and away_pick == -1):
            return
        match_request = dict(host=self.list_teamselection[home_pick],
                             guest=self.list_teamselection[away_pick])
        result = self.current_algorithm.request(match_request)
        status_text = "{}{}{}{}{}".format('Prediction for ',
                                          self.list_teamselection[home_pick],
                                          ' (host) against ',
                                          self.list_teamselection[away_pick],
                                          ' is:\n')
        status_text += '\nWin: ' + "{:.2%}".format(result.get('win'))
        status_text += '\nLose: ' + "{:.2%}".format(result.get('lose'))
        status_text += '\nDraw: ' + "{:.2%}".format(result.get('draw'))
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

    def make_current_season_list(self):
        current_year = datetime.today().year

        c = crawler_class.Crawler("https://www.openligadb.de/api")
        data_for_next_round = c.get_match_data(int(current_year))
        return data_for_next_round

    def get_seasons(self):
        """Returns a list with all the Bundesliga seasons from 2002/2003 to now."""
        current = datetime.today().year
        first_season = 2003
        all_seasons = []
        for i in range(first_season, current + 1):
            all_seasons.append(i)
        return all_seasons
    # visuals

    def return_invalid(self, status):
        """Displays a text to let the user know that an invalid input has been made."""
        status['text'] = 'Invalid input.'

    def cbb_width(self, list):
        """Calculates an appropriate size for comboboxes depending on their values."""
        return max(len(str(x)) for x in list) + 1


def initiate_gui():
    gui_object = GUI()
    gui_object.root.mainloop()


initiate_gui()
