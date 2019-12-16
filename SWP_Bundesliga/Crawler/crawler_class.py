import urllib.request
import pandas as pd
import bs4 as bs  # BeautifulSoup4 Packet

class Crawler:

    def __init__(self, url):
        self.url = url

    def get_match_data(self, year):


           url_header_xml = urllib.request.Request(
               url=self.url + "/getmatchdata/bl1/" + str(year),
               data=None,
               headers={'Content-Type': 'application/xml'}   )

           # öffnet Seite
           page = urllib.request.urlopen(url_header_xml)

           # Erstellt "xml_soup"
           soup = bs.BeautifulSoup(page, 'xml')

           # erstelle eine csv, öffne diese und schreibe die headers
           filename = "all_games_" + str(year) + ".csv"
           f = open(filename, "w")
           headers = "date, team1, team2, goals_team1, goals_team2, is_Finished , round \n"
           f.write(headers)

           # liest aus jedem gefundenem Match date, team1 ,team2 ,pointsTeam1 und pointsTeam2
           for m in soup.find_all('Match'):
               date=str(m.MatchDateTime.text)
               team1 = m.Team1.TeamName.text
               team2 = m.Team2.TeamName.text
               is_Finished = m.MatchIsFinished.text
               round = m.Group.GroupOrderID.text
               # If zum unterscheiden von endständen und halbzeitergebnissen da diese keine "vorgegebene Folge" haben
               if m.MatchIsFinished.text == "true":
                 if m.find('ResultName').text == "Endergebnis":
                   goals_team1 = m.MatchResults.MatchResult.PointsTeam1.text
                   goals_team2 = m.MatchResults.MatchResult.PointsTeam2.text
                 else:
                   goals_team1 = m.find('MatchResult').find_next('MatchResult').PointsTeam1.text
                   goals_team2 = m.find('MatchResult').find_next('MatchResult').PointsTeam2.text
                 f.write(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n" )
               else:
                   goals_team1 = ''
                   goals_team2 = ''
                   f.write( date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                    # print(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 "," + is_Finished )
           f.close()

       # holt alle Spiele aus dem angegebenen Interval "s_" Anfangs Jahr/tag, "e_" End Jahr/Tag

    def get_data(self, year, data, s_day, e_day):
        """Loads and stores a portion the wanted data into a dictionary and returns the dictionary.
        Always gets entire year which gets filter by s_day and e_day

         :param year: The year which the current data origins
         :param data: A Dictionary which holds already collected data and where the new data gets stored into
         :param s_day: Starting play day for the requested data needed
         :param e_day: Ending play day for the requested data needed

         :type year: int
         :type data: Dictionary
         :type s_day: int
         :type e_day: int

         :return: a dictionary which contains the already collected data and the new data from the year \n"""

        url_header = urllib.request.Request(
            url=self.url + "/getmatchdata/bl1/" + str(year),
            data=None,
            headers={'Content-Type': 'application/json'}
        )
        page = urllib.request.urlopen(url_header)
        matches = pd.read_json(page)
        for m in range(0, 306):
            if matches['Group'][m]['GroupOrderID'] in range(s_day, e_day + 1):
                data['date'].append(matches['MatchDateTime'][m])
                data['team1'].append(matches['Team1'][m]['TeamName'])
                data['team2'].append(matches['Team2'][m]['TeamName'])
                data['is_finished'].append(matches['MatchIsFinished'][m])
                data['play_day'].append(matches['Group'][m]['GroupOrderID'])
                if matches['MatchIsFinished'][m]:
                    if matches['MatchResults'][m][0]['ResultName'] == "Endergebnis":
                        data['goal1'].append(matches['MatchResults'][m][0]['PointsTeam1'])
                        data['goal2'].append(matches['MatchResults'][m][0]['PointsTeam2'])
                    else:
                        data['goal1'].append(matches['MatchResults'][m][1]['PointsTeam1'])
                        data['goal2'].append(matches['MatchResults'][m][1]['PointsTeam2'])
                else:
                    data['goal1'].append("-")
                    data['goal2'].append("-")
        return data

    def get_match_data_interval(self, s_year, s_day, e_year, e_day):
        """Searches the match data which are requested. First stores all data into
        a dictionary then when all data is collected Stores all the data into matches.csv File

        :param s_year: Specifies the starting year for the data
        :param s_day: Specifies the starting day in s_year
        :param e_year: Specifies the ending year for the data
        :param e_day: Specifies the ending day in e_year

        :type s_year: int
        :type s_day: int
        :type e_year: int
        :type e_day: int \n"""

        data = {'date': [],
                'team1': [],
                'team2': [],
                'is_finished': [],
                'play_day': [],
                'goal1': [],
                'goal2': []}
        if s_year == e_year:
            self.get_data(s_year, data, s_day, e_day)
        else:
            for y in range(s_year, e_year + 1):
                if y == s_year:
                    self.get_data(y, data, s_day, 34)
                else:
                    if y == e_year:
                        self.get_data(y, data, 1, e_day)
                    else:
                        self.get_data(y, data, 1, 34)
        df = pd.DataFrame(data, columns=['date', 'team1', 'team2', 'goal1', 'goal2', 'is_finished', 'play_day'])
        df.to_csv('matches.csv', index=False)

    def get_teams(self, s_year, e_year):
        """ Stores all Teams which played between s_year and e_year in bl1
        in teams.csv

         :param s_year: Specifies starting year for the Team data
         :param e_year: Specifies ending year for the Team data

         :type s_year: int
         :type e_year: int """

        team_dict = {'name': [],
                     'year': []}
        for y in range(s_year, e_year + 1):
            url_header = urllib.request.Request(
                url=self.url + "/getavailableteams/bl1/" + str(y),
                data=None,
                headers={'Content-Type': 'application/json'}
            )
            page = urllib.request.urlopen(url_header)
            teams = pd.read_json(page)
            for i in range(0, 18):
                team_dict['name'].append(teams['TeamName'][i])
                team_dict['year'].append(y)
        df = pd.DataFrame(team_dict, columns=['name', 'year'])
        df.to_csv('teams.csv', index=False)


# print(Crawler.get_teams.__doc__)
# print(Crawler.get_data.__doc__)
# print(Crawler.get_match_data_interval.__doc__)

# c = Crawler("https://www.openligadb.de/api")
# c.get_match_data_interval(2016, 1, 2016, 1)
