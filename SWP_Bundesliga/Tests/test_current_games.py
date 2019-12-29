import pytest
from socket import timeout
from _datetime import datetime
from GUI import current_games


def test_MakeCurrentSeasonMatchesList():
    assert current_games.TheCurrentLists(datetime.today().year - 1).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).MakeCurrentSeasonList() is None


def test_CheckingIfTeamsOfTheCurrentSeasonFileExist():
    assert current_games.TheCurrentLists(datetime.today().year - 1).CheckingIfMatchesOfTheCurrentSeasonFileExist() is None
    assert current_games.TheCurrentLists(datetime.today().year).CheckingIfMatchesOfTheCurrentSeasonFileExist()  is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).CheckingIfMatchesOfTheCurrentSeasonFileExist()  is None


def test_GetTheListOfTheNextRoundIfItExist():
    assert current_games.TheCurrentLists(
        datetime.today().year - 1).GetTheListOfTheNextRoundIfItExist() == \
           [['The Season 2018/2019 is Finished See you Soon in The next Season ;)']]
    #  assert current_games.TheCurrentLists(datetime.today().year).GetTheListOfTheNextRoundIfItExist()  ??
    assert current_games.TheCurrentLists(
        datetime.today().year + 1).GetTheListOfTheNextRoundIfItExist() ==\
           [['The Season 2020/2021 is not started yet. Stay tuned ;)']]
