import json
from flask import Flask

app = Flask(__name__)
app.secret_key = 'something_special'


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()

POINTS_PER_PLACE = 3
MAX_PLACE_PER_CLUB = 12
