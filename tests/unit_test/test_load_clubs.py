from utils import load_clubs


def test_load_clubs():
    data = load_clubs()
    assert type(data) is list
