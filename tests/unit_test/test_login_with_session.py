from server import app
import flask


class TestSession:

    def test_login_with_session_success(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['email'] = 'john@simplylift.co'

            response = client.post('/show_summary', data={"email": "john@simplylift.co"})
            assert flask.session['email'] == 'john@simplylift.co'
            assert response.status_code == 200

    def test_login_with_session_failed(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['email'] = 'wrong@email.com'

            response = client.post('/show_summary', data={"email": "wrong@email.com"}, follow_redirects=True)
            expected_error = "Access denied.You&#39;re email is not a valid."
            assert expected_error in response.get_data(as_text=True)
            assert response.status_code == 200
