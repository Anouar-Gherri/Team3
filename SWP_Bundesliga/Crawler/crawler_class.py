# coding=utf-8
import bs4 as bs  # BeautifulSoup4 Packet
import urllib.request


class Crawler:
    def __init__(self, url):
        # URL asu openLigaDB der art https://www.openligadb.de/api
        self.url = url

        # Für welches Jahr gesucht werden soll

    # holt alle Spiele aus einem Jahr
    # muss noch gemacht werden modifikation sodass ein Zeit Intervall gewählt werden kann
    def get_match_data(self, year):

        # notwending um xml file zu erhalten sonst json
        url_header_xml = urllib.request.Request(
            url=self.url + "/getmatchdata/bl1/" + str(year),
            data=None,
            headers={'Content-Type': 'application/xml'}  # änder von json nach xml
        )

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


    def get_match_data_interval(self, s_year, s_day, e_year, e_day):
     first=True
     filename="all_games_" + str(s_year) + "." + str(s_day) + "-" + str(e_year) + "." + str(e_day) \
             + ".csv "
     f=open(filename, "w")
     headers="date, team1, team2, goals_team1, goals_team2, is_Finished , round \n"
     f.write(headers)
     for y in range(s_year, e_year + 1):
        if y == e_year:
            for d in range(1, e_day + 1):
                url_header_xml=urllib.request.Request(
                    url=self.url + "/getmatchdata/bl1/" + str(y) + "/" + str(d),
                    data=None,
                    headers={'Content-Type': 'application/xml'}  # änder von json nach xml
                )
                # öffnet Seite
                page=urllib.request.urlopen(url_header_xml)

                # Erstellt "xml_soup"
                soup=bs.BeautifulSoup(page, 'xml')
                # liest aus jedem gefundenem Match date, team1 ,team2 ,pointsTeam1 und pointsTeam2
                for m in soup.find_all('Match'):
                    date=str(m.MatchDateTime.text)
                    team1=m.Team1.TeamName.text
                    team2=m.Team2.TeamName.text
                    is_Finished=m.MatchIsFinished.text
                    round=m.Group.GroupOrderID.text
                    # If zum unterscheiden von endständen und halbzeitergebnissen da diese keine "vorgegebene Folge" haben
                    if m.MatchIsFinished.text == "true":
                        if m.find('ResultName').text == "Endergebnis":
                            goals_team1=m.MatchResults.MatchResult.PointsTeam1.text
                            goals_team2=m.MatchResults.MatchResult.PointsTeam2.text
                        else:
                            goals_team1=m.find('MatchResult').find_next('MatchResult').PointsTeam1.text
                            goals_team2=m.find('MatchResult').find_next('MatchResult').PointsTeam2.text
                        f.write(
                            date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                    else:
                        goals_team1=''
                        goals_team2=''
                        f.write(
                            date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                        # print(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 "," + is_Finished )
            f.close()
        else:
            if first:
                for d in range(s_day, 35):
                    url_header_xml=urllib.request.Request(
                        url=self.url + "/getmatchdata/bl1/" + str(y) + "/" + str(d),
                        data=None,
                        headers={'Content-Type': 'application/xml'}  # änder von json nach xml
                    )
                    # öffnet Seite
                    page=urllib.request.urlopen(url_header_xml)

                    # Erstellt "xml_soup"
                    soup=bs.BeautifulSoup(page, 'xml')
                    # liest aus jedem gefundenem Match date, team1 ,team2 ,pointsTeam1 und pointsTeam2
                    for m in soup.find_all('Match'):
                        date=str(m.MatchDateTime.text)
                        team1=m.Team1.TeamName.text
                        team2=m.Team2.TeamName.text
                        is_Finished=m.MatchIsFinished.text
                        round=m.Group.GroupOrderID.text
                        # If zum unterscheiden von endständen und halbzeitergebnissen da diese keine "vorgegebene Folge" haben
                        if m.MatchIsFinished.text == "true":
                            if m.find('ResultName').text == "Endergebnis":
                                goals_team1=m.MatchResults.MatchResult.PointsTeam1.text
                                goals_team2=m.MatchResults.MatchResult.PointsTeam2.text
                            else:
                                goals_team1=m.find('MatchResult').find_next('MatchResult').PointsTeam1.text
                                goals_team2=m.find('MatchResult').find_next('MatchResult').PointsTeam2.text
                            f.write(
                                date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                        else:
                            goals_team1=''
                            goals_team2=''
                            f.write(
                                date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                            # print(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 "," + is_Finished )
                first=False
            else:
                for d in range(1, 35):
                    url_header_xml=urllib.request.Request(
                        url=self.url + "/getmatchdata/bl1/" + str(y) + "/" + str(d),
                        data=None,
                        headers={'Content-Type': 'application/xml'}  # änder von json nach xml
                    )
                    # öffnet Seite
                    page=urllib.request.urlopen(url_header_xml)

                    # Erstellt "xml_soup"
                    soup=bs.BeautifulSoup(page, 'xml')
                    # liest aus jedem gefundenem Match date, team1 ,team2 ,pointsTeam1 und pointsTeam2
                    for m in soup.find_all('Match'):
                        date=str(m.MatchDateTime.text)
                        team1=m.Team1.TeamName.text
                        team2=m.Team2.TeamName.text
                        is_Finished=m.MatchIsFinished.text
                        round=m.Group.GroupOrderID.text
                        # If zum unterscheiden von endständen und halbzeitergebnissen da diese keine "vorgegebene Folge" haben
                        if m.MatchIsFinished.text == "true":
                            if m.find('ResultName').text == "Endergebnis":
                                goals_team1=m.MatchResults.MatchResult.PointsTeam1.text
                                goals_team2=m.MatchResults.MatchResult.PointsTeam2.text
                            else:
                                goals_team1=m.find('MatchResult').find_next('MatchResult').PointsTeam1.text
                                goals_team2=m.find('MatchResult').find_next('MatchResult').PointsTeam2.text
                            f.write(
                                date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                        else:
                            goals_team1=''
                            goals_team2=''
                            f.write(
                                date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "," + is_Finished + "," + round + "\n")
                            # print(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 "," + is_Finished )


    def get_all_teams(self, year):
        url_header_xml = urllib.request.Request(
            url=self.url + "/getavailableteams/bl1/" + str(year),
            data=None,
            headers={'Content-Type': 'application/xml'}  # änder von json nach xml

         )

        # öffnet Seite
        page = urllib.request.urlopen(url_header_xml,timeout=)

        # Erstellt "xml_soup"
        soup = bs.BeautifulSoup(page, 'xml')

        # erstelle eine csv, öffne diese und schreibe die headers
        filename = "all_teams_" + str(year) + ".csv"
        f = open(filename, "w")
        headers = "team_name, team_short\n"
        f.write(headers)

        for t in soup.find_all('Team'):
            team_name = t.TeamName.text
            team_short = t.ShortName.text
            f.write(team_name + "," + team_short + "\n")
        f.close()
