import pytest
# pytest Test/test_cart_apis.py
@pytest.mark.abc
def test_add_cart(client, user_data, login_data, book_data, book_data1, cart_item_data1, cart_item_data,update_cart_item_data,cart_item_data2):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.post('/book/add', json=book_data1, headers=header)
    assert response.status_code == 201

    response = client.post('/cart/add', json=cart_item_data, headers=header)  # add the book to the cart items
    print(response.json())
    assert response.status_code == 201

    response = client.post('/cart/add', json=update_cart_item_data, headers=header)
    assert response.status_code == 201

    response = client.post('/cart/add',json=cart_item_data2,headers=header)
    assert response.status_code == 400


def test_get_cart(client, user_data, login_data, book_data, book_data1, cart_item_data1, update_cart_item_data,cart_item_data):
    response = client.post('/user/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/user/login', json=login_data)
    assert response.status_code == 200
    header = {'authorization': response.json()['access_token']}

    response = client.get('/cart/get', headers=header)   # cart is empty
    assert response.status_code == 400

    response = client.post('/book/add', json=book_data, headers=header)
    assert response.status_code == 201

    response = client.post('/book/add', json=book_data1, headers=header)
    assert response.status_code == 201

    response = client.post('/cart/add', json=cart_item_data, headers=header)
    assert response.status_code == 201

    response = client.post('/cart/add', json=cart_item_data1, headers=header)
    assert response.status_code == 201

    response = client.get('/cart/get', headers=header)
    assert response.status_code == 200


# @pytest.mark.abcd  # pytest -v -m abcd
# def test_get_all_cart_items_details(client, user_data, login_data, book_data, book_data1, cart_item_data, cart_item_data1):
#     response = client.post('/user/register', json=user_data)
#     assert response.status_code == 201
#
#     response = client.post('/user/login', json=login_data)
#     assert response.status_code == 200
#     header = {'authorization': response.json()['access_token']}
#
#     response = client.post('/book/add', json=book_data, headers=header)
#     assert response.status_code == 201
#
#     response = client.post('/book/add', json=book_data1, headers=header)
#     assert response.status_code == 201
#
#     response = client.post('/cart/add', json=cart_item_data, headers=header)
#     assert response.status_code == 201
#
#     response = client.post('/cart/add', json=cart_item_data1, headers=header)
#     assert response.status_code == 201
#
#     response = client.get('/cart/get/1', headers=header)
#     assert response.status_code == 200
