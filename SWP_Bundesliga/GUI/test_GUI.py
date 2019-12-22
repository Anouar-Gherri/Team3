import pytest
from GUI.GUIinterface import *


# Important: Close the gui after it opens and tests will succeed
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
    this_year = datetime.today().year
    assert new_gui.crd_to_season == this_year


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


def test_team_selection(new_gui):
    new_gui.select_crawl_from_season.set('2006')
    new_gui.select_crawl_to_season.set('2007')
    new_gui.select_crawl_from_md.set('34')
    new_gui.select_crawl_to_md.set('1')
    new_gui.start_crawler()
    new_gui.select_algorithm.current(0)
    new_gui.start_training()
    assert len(new_gui.list_teamselection) == 21
