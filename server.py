from datetime import datetime
from flask import render_template, request, redirect, flash, url_for, session
from utils import app, MAX_PLACE_PER_CLUB, POINTS_PER_PLACE, competitions, clubs


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['GET', 'POST'])
def show_summary():
    try:
        if request.method == 'POST':
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            session['email'] = club['email']
        else:
            club = [club for club in clubs if club['email'] == session['email']][0]

        if 'noOfPlacesBookedOnCompetitions' in club:
            club['totalPlaceReserved'] = sum(club['noOfPlacesBookedOnCompetitions'].values())

    except KeyError:
        return user_failed_credential_redirection(KeyError)
    except IndexError:
        return user_failed_credential_redirection(IndexError)
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if 'email' not in session:
        return user_failed_credential_redirection(KeyError)
    try:
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]

        if found_club and found_competition:
            if datetime.strptime(found_competition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
                flash(f"{found_competition['name']} is over. Book another competition.")
                return redirect(url_for('show_summary', data=session['email']))
            return render_template('booking.html', club=found_club, competition=found_competition)

    except:
        flash("Something went wrong-please try again")
        return redirect(url_for('show_summary', data=session['email']))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    if request.method != 'POST':
        return user_failed_credential_redirection(KeyError)

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    total_points_required = places_required * POINTS_PER_PLACE
    if request.method == 'POST' and places_required:
        tmp_total_points = 0
        tmp_total_places_reserved = 0
        if 'noOfPlacesBookedOnCompetitions' in club:

            if competition['name'] in club['noOfPlacesBookedOnCompetitions']:
                tmp_total_points = (int(club['noOfPlacesBookedOnCompetitions'][
                                          competition['name']]) * POINTS_PER_PLACE) + total_points_required
            tmp_total_places_reserved = sum(club['noOfPlacesBookedOnCompetitions'].values()) + places_required

        else:
            tmp_total_points = total_points_required
        if int(competition['numberOfPlaces']) < places_required or int(club['points']) < places_required or \
                tmp_total_points > MAX_PLACE_PER_CLUB or tmp_total_places_reserved > MAX_PLACE_PER_CLUB or \
                int(competition['numberOfPlaces']) == 0:
            if int(club['points']) < total_points_required:
                flash(f"Not enough points. There's only {club['points']} club points left.")
            if int(competition['numberOfPlaces']) < places_required:
                flash(f"Not enough place.There's only {competition['numberOfPlaces']} places left.")
            if places_required > MAX_PLACE_PER_CLUB or tmp_total_places_reserved > MAX_PLACE_PER_CLUB:
                flash('You can only book 12 places.')
            if int(competition['numberOfPlaces']) == 0:
                flash("There's no more place left.")

            return redirect(url_for('show_summary'))

        if 'noOfPlacesBookedOnCompetitions' in club:
            if competition['name'] in club['noOfPlacesBookedOnCompetitions']:
                club['noOfPlacesBookedOnCompetitions'][competition['name']] = int(
                    club['noOfPlacesBookedOnCompetitions'][competition['name']]) + places_required
            else:
                club['noOfPlacesBookedOnCompetitions'][competition['name']] = places_required
        else:
            club['noOfPlacesBookedOnCompetitions'] = {}
            club['noOfPlacesBookedOnCompetitions'][competition['name']] = places_required
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club['points'] = int(club['points']) - (places_required * POINTS_PER_PLACE)

        flash('Great-booking complete!')
        flash(
            f"You have succesfully booked {places_required} place. The club has only {club['points']} points left.")

        return redirect(url_for('show_summary'))
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
@app.route('/points')
def show_club_points():
    for club in clubs:
        if 'noOfPlacesBookedOnCompetitions' in club:
            club['totalPlaceReserved'] = sum(club['noOfPlacesBookedOnCompetitions'].values())
        else:
            club['totalPlaceReserved'] = 0

    return render_template('points.html', clubs=clubs, competitions=competitions)


@app.route('/reservation/<competition>')
def club_reservation(competition):
    if 'email' not in session:
        return user_failed_credential_redirection(KeyError)
    found_competition = [c for c in competitions if c['name'] == competition][0]
    return render_template('reservation.html', clubs=clubs, competition=found_competition)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def user_failed_credential_redirection(error):
    if session:
        session.clear()
    if error is KeyError:
        flash("Access denied. You're not log in.")
    else:
        flash("Access denied.You're email is not a valid.")
    return redirect(url_for('index'))
