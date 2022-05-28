from server import app


class TestRoutes:
    client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_publicPoints(self):
        response = self.client.get('/points')
        assert response.status_code == 200

    def test_loginWithEmailExisting(self):
        response = self.client.post('/showSummary', data={"email": "john@simplylift.co"})

        assert response.status_code == 200

    def test_loginWithWrongEmail(self):
        response = self.client.post('/showSummary', data={"email": "wrong@email.fr"})
        assert response.status_code == 302

    def test_purchasePlaces(self):
        response = self.client.post("/purchasePlaces", data={"competition": "Spring Festival",
                                                             "club": "Simply Lift",
                                                             "places": "1"})
        assert response.status_code == 302

    def test_competitionReservation(self):
        response = self.client.get('/reservation/Spring%20Festival')
        assert response.status_code == 200

    def test_logout(self):
        response = self.client.get('/logout')
        assert response.status_code == 302
