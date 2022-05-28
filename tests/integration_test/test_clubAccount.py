from server import app, competitions, clubs
import flask


def test_loginWithPurchasePlaces():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'

        response = client.post('/showSummary', data={"email": "john@simplylift.co"})
        assert flask.session['email'] == 'john@simplylift.co'
        assert response.status_code == 200

        client.post('/purchasePlaces',
                    data={"competition": competitions[1]['name'],
                          "club": clubs[0]['name'],
                          "places": "5"}, follow_redirects=True)
        client.post('/purchasePlaces',
                    data={"competition": competitions[0]['name'],
                          "club": clubs[0]['name'],
                          "places": "3"}, follow_redirects=True)

        expectedPoints = 8
        assert sum(clubs[0]['noOfPlacesBookedOnCompetitions'].values()) == expectedPoints


def test_checkPublicCLubPoints():
    with app.test_client() as client:
        response = client.get('/points')
        assert response.status_code == 200
        assert clubs[0]['totalPointsUsed'] == 8
        assert clubs[0]['points'] == 5


def test_checkReservationPlaceInCompetition():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'
        response = client.get('/reservation/Spring%20Festival')
        expectedClubName = 'Simply Lift'
        expectedCompetitionName = 'Spring Festival'
        assert response.status_code == 200
        assert 'Spring Festival' in clubs[0]['noOfPlacesBookedOnCompetitions']
        assert clubs[0]['noOfPlacesBookedOnCompetitions'][expectedCompetitionName] == 3
        assert clubs[0]['name'] == expectedClubName
