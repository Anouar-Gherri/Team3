import pytest
from _datetime import datetime
from GUI import current_games


def test_MakeCurrentSeasonMatchesList():
    assert current_games.TheCurrentLists(datetime.today().year - 1).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year).MakeCurrentSeasonList() is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).MakeCurrentSeasonList() is None


def test_MakeCurrentSeasonTeamsList():
    assert current_games.TheCurrentLists(datetime.today().year - 1).MakeCurrentSeasonTeamsList() is None
    assert current_games.TheCurrentLists(datetime.today().year).MakeCurrentSeasonTeamsList() is None
    assert current_games.TheCurrentLists(datetime.today().year + 1).MakeCurrentSeasonTeamsList() is None
