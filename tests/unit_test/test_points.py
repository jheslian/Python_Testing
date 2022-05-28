from server import app, clubs, competitions


class TestPoints:
    client = app.test_client()

    def test_pointsLeft(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['email'] = 'john@simplylift.co'
        response = self.client.post('/purchasePlaces',
                                    data={"competition": competitions[1]['name'],
                                          "club": clubs[0]['name'],
                                          "places": "2"})
        expected_points = 11
        expected_club = 'Simply Lift'
        expected_competition = 'Spring Festival'
        assert response.status_code == 302
        assert competitions[0]['name'] == expected_competition
        assert clubs[0]['name'] == expected_club
        assert clubs[0]['points'] == expected_points

    def test_pointsUsedSuccess(self):
        response = self.client.post('/purchasePlaces',
                                    data={"competition": competitions[1]['name'],
                                          "club": clubs[0]['name'],
                                          "places": "1"}, follow_redirects=True)
        expected_points = 3
        assert response.status_code == 200
        assert sum(clubs[0]['noOfPlacesBookedOnCompetitions'].values()) == expected_points

    def test_errorForNotEnoughPoints(self):
        response = self.client.post('/purchasePlaces',
                                    data={"competition": competitions[1]['name'],
                                          "club": clubs[1]['name'],
                                          "places": "5"}, follow_redirects=True)

        data = response.get_data(as_text=True)
        expected_error = f"Not enough points."
        assert response.status_code == 200
        assert expected_error in data

    def test_errorForMoreThan12Places(self):
        response = self.client.post('/purchasePlaces',
                                    data={"competition": competitions[1]['name'],
                                          "club": clubs[0]['name'],
                                          "places": "13"})

        data = response.get_data(as_text=True)
        expected_error = 'You can only book 12 places.'
        assert response.status_code == 200
        assert expected_error in data

    def test_errorNotEnoughPlaces(self):
        response = self.client.post('/purchasePlaces',
                                    data={"competition": competitions[1]['name'],
                                          "club": clubs[1]['name'],
                                          "places": "11"})
        data = response.get_data(as_text=True)
        expected_error = 'Not enough place.There&#39;s only 10 places left.'
        assert response.status_code == 200
        assert expected_error in data
