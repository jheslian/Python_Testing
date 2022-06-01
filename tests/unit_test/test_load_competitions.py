from utils import load_competitions


def test_load_competitions():
    data = load_competitions()
    assert type(data) is list
