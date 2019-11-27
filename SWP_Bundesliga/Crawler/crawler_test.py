import crawler_class

c1 = crawler_class.Crawler("https://www.openligadb.de/api", 2019)
c1.get_match_data()
c1.get_all_teams()