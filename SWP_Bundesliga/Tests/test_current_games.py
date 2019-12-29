import pytest
from socket import timeout
from _datetime import datetime
from GUI import current_games


@pytest.mark.current_games
def test_MakeCurrentSeasonMatchesList():
    assert current_games.TheCurrentLists(datetime.today().year - 1).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).MakeCurrentSeasonList() is None


# CheckingIfMatchesOfTheCurrentSeasonFileExist attribute doesnt exist
"""
def test_CheckingIfTeamsOfTheCurrentSeasonFileExist():
    assert current_games.TheCurrentLists(datetime.today().year - 1).CheckingIfMatchesOfTheCurrentSeasonFileExist() is None
    assert current_games.TheCurrentLists(datetime.today().year).CheckingIfMatchesOfTheCurrentSeasonFileExist()  is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).CheckingIfMatchesOfTheCurrentSeasonFileExist()  is None
"""


# Nachdem man matches.csv in den Ordner schiebt, wird das TestData(2018).csv file gelöscht und
# die anderen Test funktionieren nicht
def test_GetTheListOfTheNextRoundIfItExist():
    assert current_games.TheCurrentLists(
        datetime.today().year - 1).GetTheListOfTheNextRoundIfItExist() == \
           [['The Season 2018/2019 is Finished See you Soon in The next Season ;)']]
    #  assert current_games.TheCurrentLists(datetime.today().year).GetTheListOfTheNextRoundIfItExist()  ??
    assert current_games.TheCurrentLists(
        datetime.today().year + 1).GetTheListOfTheNextRoundIfItExist() ==\
           [['The Season 2020/2021 is not started yet. Stay tuned ;)']]
