from utils import loadClubs


def test_loadClubs():
    data = loadClubs()
    assert type(data) is list
