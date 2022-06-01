from server import app
from utils import competitions, clubs
import flask


def test_login_with_purchase_places():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'

        response = client.post('/show_summary', data={"email": "john@simplylift.co"})
        client.post('/purchase_places',
                    data={"competition": competitions[1]['name'],
                          "club": clubs[0]['name'],
                          "places": "2"}, follow_redirects=True)
        client.post('/purchase_places',
                    data={"competition": competitions[0]['name'],
                          "club": clubs[0]['name'],
                          "places": "2"}, follow_redirects=True)

        expected_places_booked = 4
        expected_points_left = 1
        assert flask.session['email'] == 'john@simplylift.co'
        assert response.status_code == 200
        assert sum(clubs[0]['noOfPlacesBookedOnCompetitions'].values()) == expected_places_booked
        assert clubs[0]['points'] == expected_points_left


def test_check_public_cLub_points():
    with app.test_client() as client:
        response = client.get('/points')
        assert response.status_code == 200
        assert clubs[0]['totalPlaceReserved'] == 4
        assert clubs[0]['points'] == 1


def test_check_reservation_place_in_competition():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'
        response = client.get('/reservation/Spring%20Festival')
        expected_club_name = 'Simply Lift'
        expected_competition_name = 'Spring Festival'
        expected_places_book_in_spring_festival = 2
        assert response.status_code == 200
        assert 'Spring Festival' in clubs[0]['noOfPlacesBookedOnCompetitions']
        assert clubs[0]['noOfPlacesBookedOnCompetitions'][
                   expected_competition_name] == expected_places_book_in_spring_festival
        assert clubs[0]['name'] == expected_club_name
