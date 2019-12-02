import pytest
import os
from GUI import *

test_GUI = GUI()

def resetAllInputs():
    test_GUI.selectCrawlFromSeason.set('')
    test_GUI.selectCrawlToSeason.set('')
    test_GUI.selectCrawlFromMatchday.set('')
    test_GUI.selectCrawlToMatchday.set('')
    test_GUI.selectHome.set('')
    test_GUI.selectAway.set('')


def test_crawlerButton_defaultSeasonFrom():
    resetAllInputs()
    test_GUI.selectCrawlToSeason.set('2005')
    test_GUI.startCrawler()
    
def test_crawlerButton_defaultSeasonTo():
    resetAllInputs()
    test_GUI.selectCrawlFromSeason.set('2018')
    test_GUI.selectCrawlToMatchday.set('3')
    test_GUI.startCrawler()
    
def test_crawlerButton_defaultMatchdayFrom():
    resetAllInputs()
    test_GUI.selectCrawlFromSeason.set('2006')
    test_GUI.selectCrawlToSeason.set('2006')
    test_GUI.selectCrawlToMatchday.set('3')
    test_GUI.startCrawler()
    
def test_crawlerButton_defaultMatchdayTo():
    resetAllInputs()
    test_GUI.selectCrawlFromSeason.set('2006')
    test_GUI.selectCrawlToSeason.set('2006')
    test_GUI.selectCrawlFromMatchday.set('30')
    test_GUI.startCrawler()
    
def test_teamSelection():
    resetAllInputs()
    test_GUI.selectCrawlFromSeason.set('2006')
    test_GUI.selectCrawlToSeason.set('2007')
    test_GUI.selectCrawlFromMatchday.set('34')
    test_GUI.selectCrawlToMatchday.set('1')
    test_GUI.startCrawler()
    test_GUI.startTraining()
    
# test with pytest
    
def pytest_crawlerButton_defaultSeasonFrom():
    test_crawlerButton_defaultSeasonFrom()
    assert test_GUI.crawledFromSeason == 2005
    
def pytest_crawlerButton_defaultSeasonTo():
    test_crawlerButton_defaultSeasonTo()
    thisYear = datetime.today().year
    assert test_GUI.crawledToSeason == thisYear
    
def pytest_crawlerButton_defaultMatchdayFrom():
    test_crawlerButton_defaultMatchdayFrom()
    result = os.path.isfile('all_games_2006.1-2006.3.csv')
    assert result == True
    
def pytest_crawlerButton_defaultMatchdayTo():
    test_crawlerButton_defaultMatchdayTo()
    result = os.path.isfile('all_games_2006.30-2006.34.csv')
    assert result == True
    
# TODO test training button (after implementation of training functionality)
    
def pytest_teamSelection():
    test_teamSelection()
    assert len(test_GUI.listTeamSelection) == 21
    
# call all tests

pytest_crawlerButton_defaultSeasonFrom()
pytest_crawlerButton_defaultSeasonTo()
pytest_crawlerButton_defaultMatchdayFrom()
pytest_crawlerButton_defaultMatchdayTo()

pytest_teamSelection()

print('All tests done. Everything is OK!') 
    