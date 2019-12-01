import crawler_class

c1 = crawler_class.Crawler("https://www.openligadb.de/api")

# alle Spiele aus dem Jahr 2015
# c1.get_match_data(2015)

# alle Teams in der BL im Jahr 2015
# c1.get_all_teams(2015)

# alle Spiele vom Jahr 2011 Spieltag 1 bis zum Jahr 2012 Spieltag 17
# c1.get_match_data_interval(2011, 1, 2012, 17)

