from server import loadCompetitions

def test_loadClubs():
    data = loadCompetitions()
    assert type(data) is list