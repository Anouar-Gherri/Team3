import pytest
from socket import timeout
from _datetime import datetime
from GUI import current_games


@pytest.mark.current_games
def test_MakeCurrentSeasonMatchesList():
    assert current_games.CurrentGames(datetime.today().year - 1).get_current_season() is None
    assert current_games.CurrentGames(datetime.today().year).get_current_season() is None
    assert current_games.CurrentGames(datetime.today().year + 1).get_current_season() is None


def test_GetTheListOfTheNextRoundIfItExist():
    assert current_games.CurrentGames(2018).get_display == \
           [['The Season 2018/2019 is Finished See you Soon in The next Season ;)']]
    #  assert current_games.TheCurrentLists(datetime.today().year).GetTheListOfTheNextRoundIfItExist()  ??
    assert current_games.CurrentGames(datetime.today().year).get_display ==\
           [['The Season 2020/2021 is not started yet. Stay tuned ;)']]
