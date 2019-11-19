import bs4 as bs  # BeautifulSoup4 Packet
import urllib.request


class Crawler:
    def __init__(self, url, year):
        # URL asu openLigaDB der art https://www.openligadb.de/api/getmatchdata/bl1/
        self.url = url

        # Für welches Jahr gesucht werden soll
        self.year = year

    def get_match_data(self):

        # notwending um xml file zu erhalten sonst json
        url_header_xml = urllib.request.Request(
            url=self.url + str(self.year),
            data=None,
            headers={'Content-Type': 'application/xml'}  # änder von json nach xml
        )

        # öffnet Seite
        page = urllib.request.urlopen(url_header_xml)

        # Erstellt "xml_soup"
        soup = bs.BeautifulSoup(page, 'xml')

        # erstelle eine csv, öffne diese und schreibe die headers
        filename = "all_games_" + str(self.year) + ".csv"
        f = open(filename, "w")
        headers = "date, team1, team2, goals_team1, goals_team2\n"
        f.write(headers)

        # liest aus jedem geundenem Match date, team1 ,team2 ,pointsTeam1 und pointsTeam2
        for m in soup.find_all('Match'):
            date = m.MatchDateTime.text
            team1 = m.Team1.TeamName.text
            team2 = m.Team2.TeamName.text

            # If zum unterscheiden von endständen und halbzitergebnissen da diese keine "vorgrgrbrnr Folge" haben
            if m.find('ResultName').text == "Endergebnis":
                goals_team1 = m.MatchResults.MatchResult.PointsTeam1.text
                goals_team2 = m.MatchResults.MatchResult.PointsTeam2.text
            else:
                goals_team1 = m.find('MatchResult').find_next('MatchResult').PointsTeam1.text
                goals_team2 = m.find('MatchResult').find_next('MatchResult').PointsTeam2.text
            f.write(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2 + "\n")
            # print(date + "," + team1 + "," + team2 + "," + goals_team1 + "," + goals_team2)
        f.close()