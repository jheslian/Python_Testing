from utils import app


class TestRoutes:
    client = app.test_client()

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_public_points(self):
        response = self.client.get('/points')
        assert response.status_code == 200

    def test_login_with_email_existing(self):
        response = self.client.post('/show_summary', data={"email": "john@simplylift.co"})

        assert response.status_code == 200

    def test_login_with_wrong_email(self):
        response = self.client.post('/show_summary', data={"email": "wrong@email.fr"}, follow_redirects=True)
        assert response.status_code == 200

    def test_purchase_places(self):
        response = self.client.post("/purchase_places", data={"competition": "Spring Festival",
                                                              "club": "Simply Lift",
                                                              "places": "1"}, follow_redirects=True)
        assert response.status_code == 200

    def test_competition_reservation(self):
        response = self.client.get('/reservation/Spring%20Festival', follow_redirects=True)
        assert response.status_code == 200

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
