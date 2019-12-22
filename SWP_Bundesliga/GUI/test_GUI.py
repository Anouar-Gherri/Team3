import pytest
<<<<<<< HEAD
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
=======
import os
from GUIinterface import *

test_GUI = GUI()

def reset_all_inputs():
    test_GUI.select_crawl_from_season.set('')
    test_GUI.select_crawl_to_season.set('')
    test_GUI.select_crawl_from_md.set('')
    test_GUI.select_crawl_to_md.set('')
    test_GUI.select_home.set('')
    test_GUI.select_away.set('')

def test_cr_button_defaultSeasonFrom():
    reset_all_inputs()
    test_GUI.select_crawl_to_season.set('2005')
    test_GUI.start_crawler()
    assert test_GUI.crd_from_season == 2005

def test_cr_button_defaultSeasonTo():
    reset_all_inputs()
    test_GUI.select_crawl_from_season.set('2018')
    test_GUI.select_crawl_to_md.set('3')
    test_GUI.start_crawler()
    this_year = datetime.today().year
    assert test_GUI.crd_to_season == this_year

def test_cr_button_defaultMDFrom():
    reset_all_inputs()
    test_GUI.select_crawl_from_season.set('2006')
    test_GUI.select_crawl_to_season.set('2006')
    test_GUI.select_crawl_to_md.set('3')
    test_GUI.start_crawler()
    assert test_GUI.crd_from_md == 1

def test_cr_button_defaultMDTo():
    reset_all_inputs()
    test_GUI.select_crawl_from_season.set('2006')
    test_GUI.select_crawl_to_season.set('2006')
    test_GUI.select_crawl_from_md.set('30')
    test_GUI.start_crawler()
    assert test_GUI.crd_to_md == 34

def test_teamselection():
    reset_all_inputs()
    test_GUI.select_crawl_from_season.set('2006')
    test_GUI.select_crawl_to_season.set('2007')
    test_GUI.select_crawl_from_md.set('34')
    test_GUI.select_crawl_to_md.set('1')
    test_GUI.start_crawler()
    test_GUI.select_algorithm.current(0)
    test_GUI.start_training()
    assert len(test_GUI.list_teamselection) == 21

# TODO test training button (after implementation of training functionality)
def call_tests():
    test_cr_button_defaultSeasonFrom()
    test_cr_button_defaultSeasonTo()
    test_cr_button_defaultMDFrom()
    test_cr_button_defaultMDTo()
    test_teamselection()

call_tests()
print('All tests done. Everything is OK!') 
>>>>>>> 9aac28039ba7b7fdce1e23fd74bcfa9672a38d21
