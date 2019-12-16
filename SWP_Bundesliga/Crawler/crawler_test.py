import crawler_class
import pytest
import pandas as pd


@pytest.fixture(scope='module')
def crawler():
    c = crawler_class.Crawler("https://www.openligadb.de/api")
    return c


@pytest.mark.parametrize('start_year, end_year',
                         [
                             (2016, 2016),
                             (2016, 2018),
                         ])
def test_get_teams(crawler, start_year, end_year):
    crawler.get_teams(start_year, end_year)
    df = pd.read_csv('teams.csv')
    assert len(df) == (end_year - start_year + 1) * 18
    assert type(df) is pd.DataFrame
    assert pd.read_csv('teams.csv').equals(pd.read_csv('teams_' + str(start_year) + '_' + str(end_year) + '.csv'))


@pytest.mark.parametrize('year, start_day, end_day',
                         [
                             (2016, 1, 1),
                             (2015, 16, 18)
                         ])
def test_get_data(crawler, year, start_day, end_day):
    data = {'date': [],
            'team1': [],
            'team2': [],
            'is_finished': [],
            'play_day': [],
            'goal1': [],
            'goal2': []}
    new_data = crawler.get_data(year, data, start_day, end_day)
    assert type(new_data) is dict
    assert len(new_data['date']) == 9 * (end_day - start_day + 1)
    """need to add data check if correct data inhere
    also need to add test to get_match_data_intervall"""