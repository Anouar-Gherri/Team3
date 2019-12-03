#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from _datetime import datetime
import csv

from Crawler import crawler_class
from builtins import int


class GUI:
    def __init__(self):
        """Builds the main window of the GUI."""
        # window properties
        self.root = Tk()
        self.root.geometry('500x400')
        self.root.title('Bundesliga Vorhersage')
        
        # structural attributes
        self.mainGrid = Frame(self.root)
        self.mainGrid.pack()
        
        self.frameCrawler = Frame(self.mainGrid)
        self.frameTeamSelection = Frame(self.mainGrid)
        self.frameNextMatchday = Frame(self.mainGrid)
        
        self.spacing = 10
        
        # crawler objects
        self.initCrawlerObjects()
        
        # training objects
        self.buttonTraining = Button(self.mainGrid, 
                                     text='Start Training', 
                                     command=self.startTraining, 
                                     state='disabled')
        
        self.statusTraining = Label(self.mainGrid, text='')
        
        # team selection objects
        self.initTeamSelectionObjects()

        # prediction objects
        self.buttonPrediction = Button(self.mainGrid,
                                       text='Start Prediction',
                                       command=self.startPrediction, 
                                       state='disabled')
        
        self.statusPrediction = Label(self.mainGrid, text='')
        
        # next matchday table
        self.initNextMatchdayTable()
        
        # position all objects
        self.frameCrawler.grid(row=0)
        self.buttonTraining.grid(row=1)
        self.statusTraining.grid(row=2)
        self.frameTeamSelection.grid(row=3)
        self.buttonPrediction.grid(row=4)
        self.statusPrediction.grid(row=5)
        self.frameNextMatchday.grid(row=6)
        
        #self.root.mainloop()  # Start the event loop
        
    def initCrawlerObjects(self):
        """Builds the GUI objects pertaining to the crawler."""
        self.listSeasons = self.getSeasons()
        self.listMatchdays = [x for x in range(1,35)]
        
        self.labelCrawlFrom = Label(self.frameCrawler, text='From:')
        self.selectCrawlFromSeason = ttk.Combobox(self.frameCrawler, 
                                                  values=self.listSeasons,
                                                  width=self.genComboboxWidth(self.listSeasons))
        self.selectCrawlFromMatchday = ttk.Combobox(self.frameCrawler, 
                                                    values=self.listMatchdays,
                                                    width=self.genComboboxWidth(self.listMatchdays))
        
        self.labelCrawlTo = Label(self.frameCrawler, text='To:')
        self.selectCrawlToSeason = ttk.Combobox(self.frameCrawler, 
                                                values=self.listSeasons,
                                                width=self.genComboboxWidth(self.listSeasons))
        self.selectCrawlToMatchday = ttk.Combobox(self.frameCrawler, 
                                                  values=self.listMatchdays,
                                                  width=self.genComboboxWidth(self.listMatchdays))
        self.buttonCrawler = Button(self.frameCrawler, 
                                    text='Start Crawler', 
                                    command=self.startCrawler)
        self.statusCrawled = Label(self.frameCrawler, text='')
        
        self.labelCrawlFrom.grid(row=0, column=0)
        self.selectCrawlFromSeason.grid(row=0, column=1)
        self.selectCrawlFromMatchday.grid(row=0, column=2)
        self.frameCrawler.grid_columnconfigure(3, minsize=self.spacing)
        self.labelCrawlTo.grid(row=0, column=4)
        self.selectCrawlToSeason.grid(row=0, column=5)
        self.selectCrawlToMatchday.grid(row=0, column=6)
        self.frameCrawler.grid_columnconfigure(7, minsize=self.spacing)
        self.buttonCrawler.grid(row=0, column=8)
        self.statusCrawled.grid(row=1, columnspan=9)
        
    def initTeamSelectionObjects(self):
        """Builds the GUI objects pertaining to the team selection."""
        
        self.labelHomeTeam = Label(self.frameTeamSelection, text='Home Team:')
        self.selectHome = ttk.Combobox(self.frameTeamSelection, width=2)
        self.selectHomeCurrent = self.selectHome.current()
        self.selectHome.bind('<<ComboboxSelected>>', self.updateSelection)
        
        self.labelAwayTeam = Label(self.frameTeamSelection, text='Away Team:')
        self.selectAway = ttk.Combobox(self.frameTeamSelection, width=2)
        self.selectAwayCurrent = self.selectAway.current()
        self.selectAway.bind('<<ComboboxSelected>>', self.updateSelection)
        
        self.labelHomeTeam.grid(row=0, column=0)
        self.selectHome.grid(row=0, column=1)
        self.labelAwayTeam.grid(row=1, column=0)
        self.selectAway.grid(row=1, column=1)
        
    def initNextMatchdayTable(self):
        self.labelNMDTitle = Label(self.frameNextMatchday, text='Next Matchday')
        self.labelNMDHome = Label(self.frameNextMatchday, text='Home Team')
        self.labelNMDAway = Label(self.frameNextMatchday, text='Away Team')
        self.labelNMDDate = Label(self.frameNextMatchday, text='Date')
        self.labelNMDTime = Label(self.frameNextMatchday, text='Time')
        
        self.labelNMDTitle.grid(row=0, columnspan=6)
        # column 0 saved for home team img 
        self.labelNMDHome.grid(row=1, column=1)
        # column 2 saved for away team img 
        self.labelNMDAway.grid(row=1, column=3)
        self.labelNMDDate.grid(row=1, column=4)
        self.labelNMDDate.grid(row=1, column=5)
        
    def initListTeams(self):
        """Sets team selection options based on crawled data."""
        self.listTeamSelection = []
        
        for year in range(self.crawledFromSeason, self.crawledToSeason+1):
            with open('all_teams_' + str(year) + '.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for team in reader:
                    if team['team_name'] not in self.listTeamSelection:
                        self.listTeamSelection.append(team['team_name'])
        self.listTeamSelection.sort()
        self.selectHome.config(values=self.listTeamSelection, 
                               width=self.genComboboxWidth(self.listTeamSelection))
        self.selectAway.config(values=self.listTeamSelection, 
                               width=self.genComboboxWidth(self.listTeamSelection))
        
    def startCrawler(self):
        """Starts the crawler after checking input values and inserting default values."""
        thisSeason = datetime.today().year
        self.crawledFromSeason = self.selectCrawlFromSeason.get()
        fromMatchday = self.selectCrawlFromMatchday.get()
        self.crawledToSeason = self.selectCrawlToSeason.get()
        toMatchday = self.selectCrawlToMatchday.get()
        # if no selection made default to current season
        if self.crawledToSeason == '':
            self.crawledToSeason = thisSeason
        elif self.selectCrawlToSeason.current() == -1:
            self.returnInvalid(self.statusCrawled)
            return
        else:
            self.crawledToSeason = int(self.crawledToSeason)
        # if no selection made default to selected crawledToSeason
        if self.crawledFromSeason == '':
            self.crawledFromSeason = self.crawledToSeason
        elif self.selectCrawlFromSeason.current() == -1:
            self.returnInvalid(self.statusCrawled)
            return
        else:
            self.crawledFromSeason = int(self.crawledFromSeason)
        # if no selection made default to first matchday
        if fromMatchday == '':
            fromMatchday = 1
        elif self.selectCrawlFromMatchday.current() == -1:
            self.returnInvalid(self.statusCrawled)
            return
        else:
            fromMatchday = int(fromMatchday)
        # if no selection made default to last matchday
        if toMatchday == '':
            toMatchday = 34
        elif self.selectCrawlToMatchday.current() == -1:
            self.returnInvalid(self.statusCrawled)
            return
        else:
            toMatchday = int(toMatchday)
            
        if (self.crawledFromSeason > self.crawledToSeason
            or (self.crawledFromSeason == self.crawledToSeason
                and fromMatchday > toMatchday)):
            self.returnInvalid(self.statusCrawled)
            return
        
        self.currentCrawl = crawler_class.Crawler("https://www.openligadb.de/api")
        self.currentCrawl.get_match_data_interval(self.crawledFromSeason, 
                                                  fromMatchday, 
                                                  self.crawledToSeason, 
                                                  toMatchday)
        
        for i in range(self.crawledFromSeason, self.crawledToSeason+1):
            self.currentCrawl.get_all_teams(i)
        
        if self.crawledFromSeason == self.crawledToSeason:
            crawledInterval = str(self.crawledFromSeason)
        else:
            crawledInterval = "{}{}{}".format(str(self.crawledFromSeason),
                                              " to ",
                                              str(self.crawledToSeason))
        
        self.statusCrawled['text'] = "{}{}{}".format("Crawling of match data from ",
                                                     crawledInterval,
                                                     " done.")
        self.buttonTraining['state'] = 'normal'
        
    def startTraining(self):
        self.statusTraining['text'] = 'Training done.'
        self.buttonPrediction['state'] = 'normal'
        self.initListTeams()
        
    def startPrediction(self):
        homePick = self.selectHome.current()
        awayPick = self.selectAway.current()
        statusText = "{}{}{}{}{}".format('Prediction for ',
                                         self.listTeamSelection[homePick],
                                         ' against ',
                                         self.listTeamSelection[awayPick],
                                         ' is...')
        if (homePick != -1 and awayPick != -1):
            self.statusPrediction['text'] = statusText
    
    def updateSelection(self, select):
        """Switches home team and away team selection if the user tries to select the same team twice."""
        if (self.selectHome.get() == self.selectAwayCurrent):
            self.selectAway.set(self.selectHomeCurrent)
            self.selectHomeCurrent = self.selectHome.get()
            self.selectAwayCurrent = self.selectAway.get()
        elif (self.selectAway.get() == self.selectHomeCurrent):
            self.selectHome.set(self.selectAwayCurrent)
            self.selectAwayCurrent = self.selectAway.get()
            self.selectHomeCurrent = self.selectHome.get()
        else:
            self.selectHomeCurrent = self.selectHome.get()
            self.selectAwayCurrent = self.selectAway.get()

    def make_current_season_list(self):
        current_year=datetime.today().year

        c=crawler_class.Crawler("https://www.openligadb.de/api")
        data_for_next_round=c.get_match_data(int(current_year))
        return data_for_next_round

    def getSeasons(self):
        """Returns a list with all the Bundesliga seasons from 2002/2003 to now."""
        current = datetime.today().year
        firstSeason = 2003
        allSeasons = []
        
        for i in range(firstSeason, current+1):
            allSeasons.append(i)

        return allSeasons

    # visuals
    
    def returnInvalid(self, status):
        """Displays a text to let the user know that an invalid input has been made."""
        status['text'] = 'Invalid input.'
    
    def genComboboxWidth(self, list):
        """Calculates an appropriate size for comboboxes depending on their values."""
        return max(len(str(x)) for x in list)+1


def initiateGUI():
    GUI_object = GUI()
    GUI_object.root.mainloop()

initiateGUI()