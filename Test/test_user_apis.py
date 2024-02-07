# pytest Test/test_user_apis.py
def test_user_registration(client, user_data, user_data_error):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/register', json=user_data_error)  # unique data violation
    assert response.status_code == 400


def test_user_login(client, user_data, login_data,login_data1):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200

    response = client.post('/user/login',json=login_data1)
    assert response.status_code == 400
