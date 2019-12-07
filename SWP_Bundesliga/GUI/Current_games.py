import csv
from _datetime import datetime
from texttable import Texttable
from pathlib import Path
from Crawler import crawler_class
import pandas as pd
from prettytable import PrettyTable
import numpy
class TheCurrentLists:
    def __init__(self,year):
        self.year = year
    def MakeCurrentSeasonList(self):
        new =crawler_class.Crawler("https://www.openligadb.de/api")
        return new.get_match_data(self.year)


    def MakeCurrentSeasonTeamsList(self):
        new =crawler_class.Crawler("https://www.openligadb.de/api")
        return new.get_all_teams(self.year)


    def CheckingIfTeamsOfTheCurrentSeasonFileExist(self):
       file = f'all_games{self.year}.csv'
       path = Path(file)
       if  path.exists() == False:
           file =  self.MakeCurrentSeasonList()
       return file


    def CheckingIfMatchesOfTheCurrentSeasonFileExist(self):
       file = f'all_games{self.year}.csv'
       path = Path(file)
       if  path.exists() == False:
           file =  self.MakeCurrentSeasonList()
       return file



    def g(self):
        df = pd.read_csv(f'all_games_{self.year}.csv',encoding = 'unicode_escape')
        IsItEmpty = df.empty
        if not IsItEmpty: #if the csv data is not empty that mean this season data are availble
           if df.empty:
               print(f'The Season {self.year}/{self.year + 1} is Finished See you Soon in The next Season ;)')
                # if all games are played and all rows in is_Finished are True that mean this season is Finished
           else:
             TheRoundsWhereMatchesAreNotCompletlyPlayed = df[min(df[' round ']) and (df[' is_Finished '] == False)]
             TheSmallestRoundWhereTheMatchesAreNotCompletlyPlayed = min(TheRoundsWhereMatchesAreNotCompletlyPlayed[' round '])
             df= TheRoundsWhereMatchesAreNotCompletlyPlayed[TheRoundsWhereMatchesAreNotCompletlyPlayed[' round '] == TheSmallestRoundWhereTheMatchesAreNotCompletlyPlayed]
             df=df.drop(df.columns[[3,4,5,6]], axis=1).reset_index(drop=True)
             list1=[]
             list2=[]
             for i in (' team1',' team2','date'):
              for idx in df.index:
                  list1.append(df.loc[idx,i])
             listlength=int(len(list1) / 3)
             for i in range(listlength):
                 list2.append(f'{list1[0 + i]} will play against {list1[listlength + i]} at this time {list1[(listlength * 2) + i]}')
             lengthlist2=len(list2)
             list2=numpy.reshape(list2, (lengthlist2, 1))
             return list2
        else: #if the csv data is empty that mean this season data are not availble
            print(f'The Season {self.year}/{self.year+1} is not started yet. \n Stay tuned ;)')

nextgamelist=TheCurrentLists(2019)
nextgamelist.CheckingIfTeamsOfTheCurrentSeasonFileExist()
ListOfTheNextGames=nextgamelist.g()
print(ListOfTheNextGames)
t=Texttable()
for i in range(2):
    t.add_row(ListOfTheNextGames[i])
print(t.draw())