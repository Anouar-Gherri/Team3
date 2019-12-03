from _datetime import datetime
import csv

class lists:
 def get_the_current_Gameday(self):
   y=datetime.today().year

   self.not_played_yet = [] # this is a temporary list
   self.allready_played = []
   with open(f'all_games_{y}.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:


            if row[5] =='true':  # check if a piece has a number in the minifig pieecs list
                self.allready_played.append(row[6,2])

            elif row[5] == 'false':
                self.not_played_yet.append(row[6])
            line_count+=1
    print(self.allready_played)
    self.not_played_yet = list(map(int, self.not_played_yet))
    self.allready_played = list(map(int, self.allready_played))

    return min(self.not_played_yet)
 def get_list_of_current_Matchday(self):
   y=datetime.today().year
   this_round = self.get_the_current_Gameday()
   self.list_current_Matchday = []
   with open(f'all_games_{y}.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
            if row[6] == this_round:
                self.list_current_Matchday.append(row[0,1,2,6])
            line_count+=1

   return self.list_current_Matchday


c=lists
new=c.get_list_of_current_Matchday()
