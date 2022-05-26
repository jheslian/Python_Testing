import json
from flask import Flask, render_template, request, redirect, flash, url_for, session


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    try:
        if request.method == 'POST':
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            session['email'] = club['email']
        else:
            club = [club for club in clubs if club['email'] == session['email']][0]
        if not club:
            return userFailedCredentialRedirection()

        if 'noOfPlacesBookedOnCompetitions' in club:
            club['totalPointsUsed'] = sum(club['noOfPlacesBookedOnCompetitions'].values())

    except KeyError:
        return userFailedCredentialRedirection()
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if 'email' not in session:
        return userFailedCredentialRedirection()
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            # return redirect(f"/book/{club}/{competition}")

            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except:
        flash("Something went wrong-please try again")
        return redirect(url_for('showSummary', data=session['email']))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    if request.method != 'POST':
        return userFailedCredentialRedirection()

    MAX_PLACE_PER_CLUB = 12
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if request.method == 'POST' and placesRequired:
        tmpTotalPoints = 0
        if 'noOfPlacesBookedOnCompetitions' in club:

            if competition['name'] in club['noOfPlacesBookedOnCompetitions']:
                tmpTotalPoints = int(club['noOfPlacesBookedOnCompetitions'][competition['name']]) + placesRequired
            # club['totalPointsUsed'] = sum(club['noOfPlacesBookedOnCompetitions'].values())
        else:

            tmpTotalPoints = placesRequired
            # club['totalPointsUsed'] = placesRequired
        if int(competition['numberOfPlaces']) < placesRequired or int(club['points']) < placesRequired or \
                tmpTotalPoints > MAX_PLACE_PER_CLUB or int(competition['numberOfPlaces']) == 0:
            if int(club['points']) < placesRequired:
                flash(f"Not enough points. There's only {club['points']} club points left.")
            if int(competition['numberOfPlaces']) < placesRequired:
                flash(f"Not enough place.There's only {competition['numberOfPlaces']} places left.")
            if placesRequired > MAX_PLACE_PER_CLUB or tmpTotalPoints > MAX_PLACE_PER_CLUB:
                flash('You can only book 12 places.')
            if int(competition['numberOfPlaces']) == 0:
                flash("There's no more place left.")

            return render_template('booking.html', club=club, competition=competition)

        """else:
            
            club['noOfPlacesBookedOnCompetitions'][competition['name']]= placesRequired"""
        if 'noOfPlacesBookedOnCompetitions' in club:
            if competition['name'] in club['noOfPlacesBookedOnCompetitions']:
                club['noOfPlacesBookedOnCompetitions'][competition['name']] = int(
                    club['noOfPlacesBookedOnCompetitions'][competition['name']]) + placesRequired
            else:
                club['noOfPlacesBookedOnCompetitions'][competition['name']] = placesRequired
        else:
            club['noOfPlacesBookedOnCompetitions'] = {}
            club['noOfPlacesBookedOnCompetitions'][competition['name']] = placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired

        flash('Great-booking complete!')
        flash(
            f"You have succesfully booked {placesRequired} place. The club has only {club['points']} points left.")

        return redirect(url_for('showSummary'))
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/points')
def showClubPoints():
    for club in clubs:
        if 'noOfPlacesBookedOnCompetitions' in club:
            club['totalPointsUsed'] = sum(club['noOfPlacesBookedOnCompetitions'].values())
        else:
            club['totalPointsUsed'] = 0

    return render_template('points.html', clubs=clubs, competitions=competitions)


@app.route('/reservation/<competition>')
def clubReservation(competition):
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    return render_template('reservation.html', clubs=clubs, competition=foundCompetition)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def userFailedCredentialRedirection():
    if session:
        session.clear()
    flash("Access denied. You're not log in or your email is not a valid.")
    return redirect(url_for('index'))

