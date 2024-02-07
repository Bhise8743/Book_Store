# pytest Test/test_books_apis.py
def test_add_book(client, user_data, login_data, book_data, book_data_error):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.post('/book/add', json=book_data_error, headers=header)   #422 Unprocessable Entity data is not in the valid formate
    assert response.status_code == 422


def test_add_book_not_super_user(client, user_data_not_super_user, login_data1, book_data, ):
    response = client.post('/user/register', json=user_data_not_super_user)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data1)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/book/add', json=book_data)  # without authorization give the forbidden client error
    assert response.status_code == 403

    response = client.post('/book/add', json=book_data,headers=header)  # this user not a super user
    assert response.status_code == 400


def test_get_book(client, user_data, login_data, book_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header_token = response.json()['access_token']
    header = {'authorization': header_token}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.get('/book/get/1', headers=header)
    assert response.status_code == 200

    response = client.get('/book/get/3', headers=header)  # this book is not exist in the database
    assert response.status_code == 400


def test_get_all_books(client, user_data, login_data, book_data, book_data1):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.post('/book/add', json=book_data1, headers=header)
    assert response.status_code == 201

    response = client.get('/book/get_all', headers=header)
    assert response.status_code == 200


def test_update_book(client, user_data, login_data, book_data, book_data1):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.put('/book/update/1', headers=header, json=book_data1)
    assert response.status_code == 200

def test_update_book_not_super_user(client,user_data_not_super_user,login_data1,book_data,user_data,login_data,book_data1):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/book/add',json=book_data,headers=header)
    assert response.status_code == 201

    response = client.post('/user/register',json=user_data_not_super_user)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data1)
    assert response.status_code == 200
    header1 = {'authorization':response.json()['access_token']}

    response = client.put('/book/update/1',headers=header1,json=book_data1)   # this user is not a super user
    assert response.status_code == 400


def test_delete_book(client, user_data, book_data, login_data, book_data1):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.post('/book/add', json=book_data1, headers=header)
    assert response.status_code == 201

    response = client.delete('/book/del/1', headers=header)
    assert response.status_code == 200


def test_delete_book_not_super_user(client,user_data,book_data,book_data1,login_data,user_data_not_super_user,login_data1):
    response = client.post('/user/register',json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data)
    assert response.status_code == 200
    header = {'authorization':response.json()['access_token']}

    response = client.post('/book/add',json=book_data,headers=header)
    assert response.status_code == 201

    response = client.post('/user/register',json=user_data_not_super_user)
    assert response.status_code == 201

    response = client.post('/user/login',json=login_data1)
    assert response.status_code == 200
    header1 = {'authorization':response.json()['access_token']}

    response = client.delete('/book/del/1',headers=header1)   # not a super user
    assert response.status_code == 400

