from server import app


def test_loginWithEmailExisting():
    client = app.test_client()
    response = client.post('/showSummary', data={"email": "john@simplylift.co"})
    assert response.status_code == 200


def test_loginWithWrongEmail():
    client = app.test_client()
    response = client.post('/showSummary', data={"email": "test@test.fr"})
    assert response.status_code == 302


def test_loginWithEmptyString():
    client = app.test_client()
    response = client.post('/showSummary', data={"email": ""})
    assert response.status_code == 302
