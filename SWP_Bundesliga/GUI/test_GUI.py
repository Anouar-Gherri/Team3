import pytest
from GUI.GUIinterface import *
from Algorithm import algorithm1
from GUI import GUIinterface


@pytest.fixture()
def new_gui():
    new_gui = GUI()
    return new_gui


@pytest.mark.guitest
def test_cr_button_default_season_from(new_gui):
    new_gui.select_crawl_to_season.set('2005')
    new_gui.start_crawler()
    assert new_gui.crd_from_season == 2005


def test_cr_button_default_season_to(new_gui):
    new_gui.select_crawl_from_season.set('2018')
    new_gui.select_crawl_to_md.set('3')
    new_gui.start_crawler()
    current_season = new_gui.list_seasons[-1]
    assert new_gui.crd_to_season == current_season


def test_cr_button_default_md_from(new_gui):
    new_gui.select_crawl_from_season.set('2006')
    new_gui.select_crawl_to_season.set('2006')
    new_gui.select_crawl_to_md.set('3')
    new_gui.start_crawler()
    assert new_gui.crd_from_md == 1


def test_cr_button_default_md_to(new_gui):
    new_gui.select_crawl_from_season.set('2006')
    new_gui.select_crawl_to_season.set('2006')
    new_gui.select_crawl_from_md.set('30')
    new_gui.start_crawler()
    assert new_gui.crd_to_md == 34


def test_algorithm_selection(new_gui):
    new_gui.select_crawl_from_season.set('2008')
    new_gui.select_crawl_to_season.set('2008')
    new_gui.start_crawler()
    new_gui.select_algorithm.set('RelativeFrequencyAlgorithm')
    new_gui.start_training()
    new_gui.select_home.set('Arminia Bielefeld')
    new_gui.select_away.set('Bayer Leverkusen')
    new_gui.start_prediction()
    result_gui = new_gui.is_trained[0]

    rfa = algorithm1.create()
    rfa.train('matches.csv')
    result_algorithm = rfa.request(
        dict(
            host='Arminia Bielefeld',
            guest='Bayer Leverkusen'))
    assert result_algorithm == result_gui


def test_team_selection(new_gui):
    new_gui.select_crawl_from_season.set('2006')
    new_gui.select_crawl_to_season.set('2007')
    new_gui.start_crawler()
    new_gui.select_algorithm.current(0)
    new_gui.start_training()
    assert len(new_gui.list_teamselection) == 21


def test_current_season(new_gui):
    this_year = datetime.today().year
    assert is_season_finished(this_year - 5)
    assert is_season_finished(this_year + 2) is False
