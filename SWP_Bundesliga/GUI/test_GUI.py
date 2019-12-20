import pytest
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
