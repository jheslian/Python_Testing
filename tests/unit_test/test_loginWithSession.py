from server import app
import flask


class TestSession:

    def test_loginWithSession(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['email'] = 'john@simplylift.co'

            response = client.post('/showSummary', data={"email": "john@simplylift.co"})
            assert flask.session['email'] == 'john@simplylift.co'
            assert response.status_code == 200
