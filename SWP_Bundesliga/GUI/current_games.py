
from pathlib import Path
from Crawler import crawler_class
import pandas as pd
import numpy
from datetime import datetime
from _datetime import date


class CurrentGames:
    def __init__(self, year):
        self.year = year

    # Make a list of the matches of the  (year) season
    def get_current_season(self):
        new = crawler_class.Crawler("bl1")
        return new.get_match_data_interval(self.year, 1, self.year, 34)

    @property
    def get_display(self) -> list:
        """Returns a list of the next matches or a string (message) if none available."""
        self.get_current_season()
        df = pd.read_csv(f'matches.csv', encoding='utf-8')
        is_it_empty = df.empty
        display = []
        match_up = []
        # if the csv data is not empty that mean this season data are available
        # the_rounds_where_matches_are_not_completely_played is shorten to
        # round_not_complete
        if not is_it_empty:
            round_not_complete = df[min(df['play_day']) & (df['is_finished'] == False) 
                                    & (df['date'] > str(datetime.today()))]
            # if all games have been played
            if round_not_complete.empty:
                display.append(
                    f'The Season {self.year}/{self.year + 1} is Finished See you Soon in The next Season ;)')
                display = numpy.reshape(display, (1, 1))
                return display
            else:
                # if the current season is currently not finished then return a list with the next round
                # the_smallest_round_where_the_matches_are_not_completely_played is shorten to smallest_round
                # the_rounds_where_matches_are_not_completely_played is shorten
                # to round_not_complete
                smallest_round = min(round_not_complete['play_day'])
                df = round_not_complete[round_not_complete['play_day']
                                        == smallest_round]
                df = df.drop(df.columns[[3, 4, 5, 6]],
                             axis=1).reset_index(drop=True)
                list1 = []
                for i in ('team1', 'team2', 'date'):
                    for idx in df.index:
                        list1.append(df.loc[idx, i])
                list_length = int(len(list1) / 3)
                for i in range(list_length):
                    date = list1[(list_length * 2) + i]
                    time_slot = date.split("T")
                    display.append({'host': list1[0 + i],
                                    'guest': list1[list_length + i],
                                    'date': time_slot[0],
                                    'time': time_slot[1][0:5]})
                    match_up.append([list1[0 + i], list1[list_length + i]])
                return display, match_up
        else:  # if no new season data
            display.append(
                f'The Season {self.year}/{self.year + 1} is not started yet. Stay tuned ;)')
            display = numpy.reshape(display, (1, 1))
            return display
