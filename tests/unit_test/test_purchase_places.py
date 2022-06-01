from utils import app, clubs, competitions


class TestPurchasePlaces:
    client = app.test_client()
    test_competitions = competitions
    test_clubs = clubs

    def test_points_left(self):
        with self.client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'
        response = self.client.post('/purchase_places',
                                    data={"competition": self.test_competitions[1]['name'],
                                          "club": self.test_clubs[0]['name'],
                                          "places": "2"}, follow_redirects=True)
        expected_points_left = 7
        expected_club = 'Simply Lift'
        expected_competition = 'Spring Festival'
        assert response.status_code == 200
        assert self.test_competitions[0]['name'] == expected_competition
        assert self.test_clubs[0]['name'] == expected_club
        assert self.test_clubs[0]['points'] == expected_points_left

    def test_total_places_reserve(self):
        response = self.client.post('/purchase_places',
                                    data={"competition": self.test_competitions[1]['name'],
                                          "club": self.test_clubs[0]['name'],
                                          "places": "1"}, follow_redirects=True)
        expected_places_booked = 3
        assert response.status_code == 200
        assert sum(self.test_clubs[0]['noOfPlacesBookedOnCompetitions'].values()) == expected_places_booked

    def test_error_for_not_enough_points(self):
        response = self.client.post('/purchase_places',
                                    data={"competition": self.test_competitions[1]['name'],
                                          "club": self.test_clubs[1]['name'],
                                          "places": "5"}, follow_redirects=True)

        data = response.get_data(as_text=True)
        expected_error = f"Not enough points."
        assert response.status_code == 200
        assert expected_error in data

    def test_error_for_more_than12_places(self):
        response = self.client.post('/purchase_places',
                                    data={"competition": self.test_competitions[0]['name'],
                                          "club": self.test_clubs[0]['name'],
                                          "places": "11"}, follow_redirects=True)

        data = response.get_data(as_text=True)
        expected_error = 'You can only book 12 places.'
        assert response.status_code == 200
        assert expected_error in data

    def test_error_not_enough_places(self):
        response = self.client.post('/purchase_places',
                                    data={"competition": self.test_competitions[1]['name'],
                                          "club": self.test_clubs[1]['name'],
                                          "places": "11"}, follow_redirects=True)
        data = response.get_data(as_text=True)
        expected_error = 'Not enough place.There&#39;s only 10 places left.'
        assert response.status_code == 200
        assert expected_error in data

    def test_passed_competition_should_failed(self):
        with self.client.session_transaction() as session:
            session['email'] = 'john@simplylift.co'
        response = self.client.get(f"/book/{self.test_competitions[0]['name']}/{self.test_clubs[1]['name']}",
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        expectedError = f"{self.test_competitions[0]['name']} is over. Book another competition."
        assert response.status_code == 200
        assert expectedError in data
