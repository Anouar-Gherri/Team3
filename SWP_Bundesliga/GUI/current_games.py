
from pathlib import Path
from Crawler import crawler_class
import pandas as pd
import numpy


class TheCurrentLists:
    def __init__(self, year):
        self.year = year

    # Make a list of the matches of the  (year) season
    def MakeCurrentSeasonList(self):
        new = crawler_class.Crawler("https://www.openligadb.de/api")
        return new.get_match_data_interval(self.year, 1, self.year, 34)

    """
    # Make a list of the Teams of the (year) season
    def MakeCurrentSeasonTeamsList(self):
        new = crawler_class.Crawler("https://www.openligadb.de/api")
        return new.get_all_teams(self.year)


 # Check if the csv file exist with the current season Teams
    def CheckingIfTeamsOfTheCurrentSeasonFileExist(self):
        file = f'all_games{self.year}.csv'
        path = Path(file)
        if not path.exists():
            file = self.MakeCurrentSeasonList()
        print(file)
        return file

    """

    # Give a list of the next round if it exist otherwise a list with the
    # appropriate string
    def GetTheListOfTheNextRoundIfItExist(self) -> list:
        self.MakeCurrentSeasonList()
        df = pd.read_csv(f'matches.csv', encoding='utf-8')
        is_it_empty = df.empty
        list2 = []
        # if the csv data is not empty that mean this season data are available
        # the_rounds_where_matches_are_not_completely_played is shorten to
        # round_not_completely
        if not is_it_empty:
            round_not_completely = df[min(df['play_day']) and (
                df['is_finished'] == False)]
            # if all games are played and all rows in is_Finished are True that mean this season is Finished then return
            # a list with the appropriate message
            if round_not_completely.empty:
                list2.append(
                    f'The Season {self.year}/{self.year + 1} is Finished See you Soon in The next Season ;)')
                list2 = numpy.reshape(list2, (1, 1))
                return list2
            else:
                # if the current season is currently not finished then return a list with the next round
                # the_smallest_round_where_the_matches_are_not_completely_played is shorten to smallest_round
                # the_rounds_where_matches_are_not_completely_played is shorten
                # to round_not_completely
                smallest_round = min(round_not_completely['play_day'])
                df = round_not_completely[round_not_completely['play_day']
                                          == smallest_round]
                df = df.drop(df.columns[[3, 4, 5, 6]],
                             axis=1).reset_index(drop=True)
                list1 = []
                for i in ('team1', 'team2', 'date'):
                    for idx in df.index:
                        list1.append(df.loc[idx, i])
                listlength = int(len(list1) / 3)
                for i in range(listlength):
                    datetime = list1[(listlength * 2) + i]
                    data = datetime.split("T")
                    list2.append(
                        f'{list1[0 + i]} will play against {list1[listlength + i]} on {data[0]} at this time {data[1]}')
                lengthlist2 = len(list2)
                list2 = numpy.reshape(list2, (lengthlist2, 1))
                return list2
        else:  # if the csv data is empty that mean this season data are not available
            list2.append(
                f'The Season {self.year}/{self.year + 1} is not started yet. Stay tuned ;)')
            list2 = numpy.reshape(list2, (1, 1))
            return list2
