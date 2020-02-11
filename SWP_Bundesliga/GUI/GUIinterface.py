#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from _datetime import datetime
import csv
from Crawler import crawler_class
from builtins import int
from GUI.current_games import CurrentGames
from Algorithm import algorithm_dict
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

        # frames
        self.frame_config = Frame(self.main_grid)
        self.frame_current = Frame(self.main_grid)
        self.frame_teamselection = Frame(self.main_grid)
        self.frame_prediction = Frame(self.main_grid)
        self.frame_NMD = Frame(self.main_grid)
        self.spacing = 10

        # crawler objects
        self.list_leagues = {'1. Bundesliga': 'bl1',
                             '2. Bundesliga': 'bl2',
                             '3. Bundesliga': 'bl3', }
        leagues = [x for x in self.list_leagues.keys()]
        self.label_league = Label(self.frame_config, text='League: ')
        self.select_league = ttk.Combobox(
            self.frame_config,
            values=leagues,
            width=cbb_width(leagues),
            state='readonly')
        self.label_crawl_from = Label(self.frame_config, text='From:')
        self.select_crawl_from_season = ttk.Combobox(
            self.frame_config, values=[], width=cbb_width([]))
        self.select_crawl_from_md = ttk.Combobox(
            self.frame_config, width=cbb_width([]))
        self.label_crawl_to = Label(self.frame_config, text='To:')
        self.select_crawl_to_season = ttk.Combobox(
            self.frame_config, values=[], width=cbb_width([]))
        self.select_crawl_to_md = ttk.Combobox(
            self.frame_config, width=cbb_width([]))
        self.button_crawler = Button(
            self.frame_config,
            text='Start Crawler',
            command=self.start_crawler)
        self.status_crawled = Label(self.frame_config, text='')
        self.label_current_dataset = Label(self.frame_current, text='')
        self.crd_from_season = None
        self.crd_to_season = None
        self.crd_from_md = None
        self.crd_to_md = None

        # training objects
        self.dict_algorithm = algorithm_dict.create_algorithms()
        self.list_algorithms = [name for name in self.dict_algorithm.keys()]
        self.list_algorithms.insert(0, 'Train all')
        self.is_trained = []
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
        self.button_training = Button(self.frame_config,
                                      text='Start Training',
                                      command=self.start_training,
                                      state='disabled')
        self.status_training = Label(self.frame_config, text='')
        self.label_current_algorithm = Label(self.frame_current, text='')
        self.current_algorithm = None

        # team selection objects
        self.label_hometeam = Label(
            self.frame_teamselection,
            text='Home Team:')
        self.select_home = ttk.Combobox(
            self.frame_teamselection, width=2, state='readonly')
        self.select_home_current = self.select_home.current()
        self.label_away_team = Label(
            self.frame_teamselection,
            text='Away Team:')
        self.select_away = ttk.Combobox(
            self.frame_teamselection, width=2, state='readonly')
        self.select_away_current = self.select_away.current()
        self.list_team_selection = []

        # prediction objects
        self.button_prediction = Button(self.frame_prediction,
                                        text='Start Prediction',
                                        command=self.start_prediction,
                                        state='disabled')
        self.status_prediction = Label(self.frame_prediction, text='\n\n')
        self.frame_result_table = Frame(self.frame_prediction)

        # load all gui objects
        self.init_crawler_objects()
        self.init_training_objects()
        self.init_team_selection_objects()
        self.init_prediction_objects()
        # load next matchday table
        self.init_nmd_table()
        # position all objects
        self.frame_config.grid(row=0)
        self.frame_current.grid(row=1)
        self.frame_teamselection.grid(row=2)
        self.frame_prediction.grid(row=3)
        self.frame_NMD.grid(row=4)

    def init_crawler_objects(self):
        """Configuration and positioning of GUI objects that pertain to the crawler."""
        self.select_league.current(0)
        self.select_league.bind('<<ComboboxSelected>>', self.update_smd)
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
        self.label_current_dataset.grid(row=0)

    def init_training_objects(self):
        """Configuration and positioning of GUI objects that pertain to the training."""
        for algo in range(len(self.list_algorithms) - 1):
            self.is_trained.append(None)
        self.select_algorithm.current(0)
        self.update_smd(None)
        self.frame_algorithm.grid(row=1, column=3, columnspan=7)
        self.label_algorithm.grid(row=0, column=0)
        self.select_algorithm.grid(row=0, column=1)
        self.button_training.grid(row=1, column=11)
        self.status_training.grid(row=1, column=12)
        self.label_current_algorithm.grid(row=1)

    def init_team_selection_objects(self):
        """Configuration and positioning of GUI objects that pertain to the team selection."""
        self.select_home.bind('<<ComboboxSelected>>', self.update_selection)
        self.select_away.bind('<<ComboboxSelected>>', self.update_selection)
        self.label_hometeam.grid(row=0, column=0)
        self.select_home.grid(row=0, column=1)
        self.label_away_team.grid(row=1, column=0)
        self.select_away.grid(row=1, column=1)

    def init_prediction_objects(self):
        """Positioning of GUI objects that pertain to the match prediction."""
        self.button_prediction.grid(row=0)
        self.status_prediction.grid(row=1)
        self.frame_result_table.grid(row=2)
        Label(self.frame_prediction, text='').grid(row=3)

    def init_nmd_table(self):
        """Builds table displaying next matchday."""
        year = get_current_season("bl1")
        nmd_data = CurrentGames(year)
        nmd_table = nmd_data.get_display[0]
        list_length = len(nmd_table)
        # get training data 
        crawler_class.Crawler("bl1").get_match_data_interval(year - 9, 1, year - 1, 34)
        self.dict_algorithm.get('PoissonAlgorithm').train('matches.csv')
        crawler_class.Crawler("bl1").get_teams(year - 9, year - 1)
        valid_teams = []
        with open('teams.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for team in reader:
                valid_teams.append(team['name'])
        for a in range(list_length + 2):
            if list_length == 1 and isinstance(nmd_table[0], str):
                Label(self.frame_NMD, text=nmd_table[0])
            else:
                if a == 0:
                    Label(
                        self.frame_NMD,
                        text='Next Matches will be:').grid(
                        row=a,
                        columnspan=7)
                    continue
                if a == 1:
                    host = 'Host'
                    guest = 'Guest'
                    date = 'Date'
                    time = 'Time'
                    prediction_win = 'Win %'
                    prediction_lose = 'Lose %'
                    prediction_draw = 'Draw %'
                else:
                    host = nmd_table[a - 2]['host']
                    guest = nmd_table[a - 2]['guest']
                    date = nmd_table[a - 2]['date']
                    time = nmd_table[a - 2]['time']
                    if (host in valid_teams) and (guest in valid_teams):
                        match_request = dict(
                            host=host, guest=guest)
                        result = self.dict_algorithm['PoissonAlgorithm'].request(
                            match_request)
                        prediction_win = "{:.2%}".format(result.get('win'))
                        prediction_lose = "{:.2%}".format(result.get('lose'))
                        prediction_draw = "{:.2%}".format(result.get('draw'))
                    else:
                        prediction_win = 'n/a'
                        prediction_lose = 'n/a'
                        prediction_draw = 'n/a'
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=date).grid(
                    row=a,
                    column=0,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=time).grid(
                    row=a,
                    column=1,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=host).grid(
                    row=a,
                    column=2,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=guest).grid(
                    row=a,
                    column=3,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=prediction_win).grid(
                    row=a,
                    column=4,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=prediction_lose).grid(
                    row=a,
                    column=5,
                    sticky=N + S + E + W)
                Label(
                    self.frame_NMD,
                    relief=GROOVE,
                    text=prediction_draw).grid(
                    row=a,
                    column=6,
                    sticky=N + S + E + W)
                self.frame_NMD.grid_columnconfigure(0, minsize=70)
                self.frame_NMD.grid_columnconfigure(1, minsize=50)
                self.frame_NMD.grid_columnconfigure(4, minsize=70)
                self.frame_NMD.grid_columnconfigure(5, minsize=70)
                self.frame_NMD.grid_columnconfigure(6, minsize=70)

    def init_list_teams(self):
        """Sets team selection options based on crawled data."""
        self.list_team_selection = []
        with open('teams.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for team in reader:
                if team['name'] not in self.list_team_selection:
                    self.list_team_selection.append(team['name'])
        self.list_team_selection.sort()
        self.select_home.config(values=self.list_team_selection,
                                width=cbb_width(self.list_team_selection))
        self.select_away.config(values=self.list_team_selection,
                                width=cbb_width(self.list_team_selection))
        self.select_home.set('')
        self.select_away.set('')

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
        current_crawl = crawler_class.Crawler(league)
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
            self.crd_to_md = current_crawl.get_group_size(2018)
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
        current_crawl.get_match_data_interval(self.crd_from_season,
                                              self.crd_from_md,
                                              self.crd_to_season,
                                              self.crd_to_md)
        current_crawl.get_teams(self.crd_from_season, self.crd_to_season)
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
        if home_pick == -1 or away_pick == -1:
            return
        match_request = dict(host=self.list_team_selection[home_pick],
                             guest=self.list_team_selection[away_pick])
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
                self.is_trained[a - 1] = self.dict_algorithm[self.list_algorithms[a]].request(match_request)
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
                                          self.list_team_selection[home_pick],
                                          ' (host) against ',
                                          self.list_team_selection[away_pick],
                                          ' is:\n')
        self.status_prediction['text'] = status_text

    def update_selection(self, select):
        """Switches home team and away team selection if the user tries to select the same team twice."""
        if self.select_home.get() == self.select_away_current:
            self.select_away.set(self.select_home_current)
            self.select_home_current = self.select_home.get()
            self.select_away_current = self.select_away.get()
        elif self.select_away.get() == self.select_home_current:
            self.select_home.set(self.select_away_current)
            self.select_away_current = self.select_away.get()
            self.select_home_current = self.select_home.get()
        else:
            self.select_home_current = self.select_home.get()
            self.select_away_current = self.select_away.get()

    def update_smd(self, s):
        """Updates matchday selection according to selected league."""
        league = self.list_leagues.get(self.select_league.get())
        crawler = crawler_class.Crawler(league)
        seasons = get_seasons(league)
        md = [x for x in range(1, crawler.get_group_size(2018) + 1)]
        self.select_crawl_from_season.config(values=seasons,
                                             width=cbb_width(seasons))
        self.select_crawl_from_season.set(seasons[-2])
        self.select_crawl_to_season.config(values=seasons,
                                           width=cbb_width(seasons))
        self.select_crawl_to_season.set(seasons[-2])
        self.select_crawl_from_md.config(values=md,
                                         width=cbb_width(md))
        self.select_crawl_from_md.current(0)
        self.select_crawl_to_md.config(values=md,
                                       width=cbb_width(md))
        self.select_crawl_to_md.set(md[-1])


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
    max_md = crawler.get_group_size(year)
    last_match = crawler.get_data(year, data, 1, max_md)
    if last_match['is_finished'] and all(last_match['is_finished']):
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


def cbb_width(ls):
    """Calculates an appropriate size for comboboxes depending on their values."""
    return 1 if not ls else max(len(str(x)) for x in ls) + 1


def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.request.URLError:
        return False


def initiate_gui():
    if internet_on():
        gui_object = GUI()
        gui_object.root.mainloop()
    else:
        return print('NO INTERNET')


if __name__ == '__main__':
    initiate_gui()
