#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk

class startGUI:
    def __init__(self):
        # window items
        self.root = Tk()
        self.root.geometry('500x400')
        self.root.title('Bundesliga Vorhersage')
        
        # crawler items
        self.buttonCrawler = Button(self.root, 
                                    text='Start Crawler', 
                                    command=self.startCrawler)
        self.buttonCrawler.pack()
        
        self.statusCrawled = Label(self.root, text='')
        self.statusCrawled.pack()
        
        # training items
        self.buttonTraining = Button(self.root, 
                                     text='Start Training', 
                                     command=self.startTraining, 
                                     state='disabled')
        self.buttonTraining.pack()
        
        self.statusTraining = Label(self.root, text='')
        self.statusTraining.pack()
        
        # team selection items
        
        # TODO label, structure
        
        self.teamList = ['A', 'B', 'C', 'D','E']
        
        self.labelHomeTeam = Label(self.root, text='Home Team:')
        self.labelHomeTeam.pack()
        
        self.selectHome = ttk.Combobox(self.root, values=self.teamList)
        self.selectHome.bind('welcome', self.updateSelection)
        self.selectHome.pack()
        
        self.labelAwayTeam = Label(self.root, text='Away Team:')
        self.labelAwayTeam.pack()
        
        self.selectAway = ttk.Combobox(self.root, values=self.teamList)
        self.selectAway.bind('<<ComboboxSelected>>', self.updateSelection)
        self.selectAway.pack()
        
        # prediction items
        self.buttonPrediction = Button(self.root,
                                       text='Start Prediction',
                                       command=self.startPrediction, 
                                       state='disabled')
        self.buttonPrediction.pack()
        
        self.statusPrediction = Label(self.root, text='')
        self.statusPrediction.pack()
        
        self.root.mainloop()  # Start the event loop
        
    def startCrawler(self):
        self.statusCrawled['text'] = 'Crawling done.'
        self.buttonCrawler['state'] = 'disabled'
        self.buttonTraining['state'] = 'normal'
        
    def startTraining(self):
        self.statusTraining['text'] = 'Training done.'
        self.buttonPrediction['state'] = 'normal'
        
    def startPrediction(self):
        homePick = self.selectHome.get()
        awayPick = self.selectAway.get()
        statusText = 'Prediction for '+ homePick +' against '+ awayPick + " is..."
        if (homePick != '' and homePick in self.teamList
            and awayPick != '' and awayPick in self.teamList):
            self.statusPrediction['text'] = statusText
    
    # make it impossible to select the same team as home and away team 
    def updateSelection(self, select):
        newHome = [el for el in self.teamList if el is not self.selectAway.get()]
        newAway = [el for el in self.teamList if el is not self.selectHome.get()]
        self.selectHome.config(values=newHome)
        self.selectAway.config(values=newAway)
        
        
startGUI()
