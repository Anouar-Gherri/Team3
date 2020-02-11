import crawler_class
import pytest
import pandas as pd


@pytest.fixture(scope='module')
def crawler():
    c = crawler_class.Crawler("bl1")
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
    assert pd.read_csv('teams.csv').equals(
        pd.read_csv('test_file/teams_' + str(start_year) + '_' + str(end_year) + '.csv'))


@pytest.mark.parametrize('year, start_day, end_day, res',
                         [
                             (2016, 1, 1, pd.read_csv(
                                 'test_file/dict_2016_1_1.csv')),
                             (2010, 16, 18, pd.read_csv(
                                 'test_file/dict_2010_16_18.csv'))
                         ])
def test_get_data(crawler, year, start_day, end_day, res):
    data = {'date': [],
            'team1': [],
            'team2': [],
            'is_finished': [],
            'play_day': [],
            'goal1': [],
            'goal2': []}
    new_data = crawler.get_data(year, data, start_day, end_day)
    new_df = pd.DataFrame(new_data, columns=['date', 'team1', 'team2', 'goal1', 'goal2', 'is_finished', 'play_day'])
    assert type(new_data) is dict
    assert len(new_data) == 7
    assert len(new_data['date']) == len(new_data['team1']) == \
           len(new_data['team2']) == len(new_data['is_finished']) == \
           len(new_data['play_day']) == len(new_data['goal1']) == len(new_data['goal2'])
    assert res.equals(new_df)


@pytest.mark.parametrize('start_year,end_year, start_day, end_day, res',
                         [
                             (2016, 2016, 1, 1, pd.read_csv('test_file/dict_2016_1_1.csv')),
                             (2010, 2010, 16, 18, pd.read_csv('test_file/dict_2010_16_18.csv')),
                             (2012, 2013, 34, 1, pd.read_csv('test_file/df_2012_2013_34_1.csv')),
                             (2012, 2014, 34, 1, pd.read_csv('test_file/df_2012_2014_34_1.csv')),
                             (2000, 2000, 1, 34, pd.read_csv('test_file/df_empty.csv'))
                         ])
def test_interval(crawler, start_year, end_year, start_day, end_day, res):
    crawler.get_match_data_interval(start_year, start_day, end_year, end_day)
    assert pd.read_csv('matches.csv').equals(res)


@pytest.mark.parametrize('crw,year,res',
                         [
                             ('bl1', 2016, 34),
                             ('bl2', 2010, 34),
                             ('bl3', 2013, 38),
                             ('bl1', 2000, 0)
                         ])
def test_group_size(crw, year, res):
    c = crawler_class.Crawler(crw)
    assert c.get_group_size(year) == res
