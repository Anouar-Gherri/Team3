import csv
from _datetime import datetime
from pathlib import Path
from Crawler import crawler_class
import pandas as pd

class Lists:
    def __init__(self, year):
        self.year = year

    def MakeCurrentSeasonList(self):
        new =crawler_class.Crawler("https://www.openligadb.de/api")
        return new.get_match_data(self.year)


    def CheckingIfFileExist(self):
       file = f'all_games{self.year}.csv'
       path = Path(file)
       if  path.exists() == False:
           file =  self.MakeCurrentSeasonList()
       return file



    def g(self,teams_number):
        df=pd.read_csv("all_games_2019.csv",encoding = 'unicode_escape')
        result1 =df[min(df[' round ']) and (df[' is_Finished '] == False)]
        result2=result1.head(int(teams_number/2))
        result3=result2.to_dict().values()
        return result3

c=Lists(datetime.today().year)
c.CheckingIfFileExist()
c.g(18)
