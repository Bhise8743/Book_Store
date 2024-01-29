# from fastapi.testclient import TestClient
# import pytest
# from sqlalchemy.orm import Session, sessionmaker
# from sqlalchemy import create_engine
# from Core.setting import postgresSQL_password
# from main import app
# from Core.model import get_db, Base
#
# engine = create_engine(f'postgresql+psycopg2://postgres:{postgresSQL_password}@localhost:5432/Test_Book_Store')
# session = Session(engine)
#
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# app.dependency_overrides[get_db] = override_get_db
#
# @pytest.fixture
# def client():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#
#
# def test_user_registration(client, user_data):
#     response = client.post('/user/register', json=user_data)
#     assert response.status_code == 201
#
#
# def test_user_login(client, user_data, login_data):
#     response = client.post('/user/register', json=user_data)
#     assert response.status_code == 201
#
#     response = client.post('/user/login', json=login_data)
#     assert response.status_code == 200
#
#
# # ------------------------------------------------------------------------------------------------------------------------
# def test_add_book(client, user_data, login_data, book_data):
#     response = client.post('/user/register', json=user_data)
#     assert response.status_code == 201
#
#     response = client.post('/user/login', json=login_data)
#     assert response.status_code == 200
#     header_token = response.json()['access_token']
#     header = {'authorization': header_token}
#
#     response = client.post('/book/add', json=book_data, headers=header)
#     assert response.status_code == 201
#
#
# def test_get_book(client, user_data, login_data, book_data):
#     response = client.post('/user/register', json=user_data)
#     assert response.status_code == 201
#
#     response = client.post('/user/login', json=login_data)
#     assert response.status_code == 200
#     header_token = response.json()['access_token']
#     header = {'authorization': header_token}
#
#     response = client.post('/book/add', json=book_data, headers=header)
#     assert response.status_code == 201
#
#     response = client.get('/book/get/1', headers=header)
#     assert response.status_code == 200
#
#
# def test_get_all_books(client, user_data, login_data, book_data, book_data1):
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
#     response = client.get('/book/get_all', headers=header)
#     assert response.status_code == 200
#
#
# def test_update_book(client, user_data, login_data, book_data, book_data1):
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
#     response = client.put('/book/update/1', headers=header, json=book_data1)
#     assert response.status_code == 200
#
#
# def test_delete_book(client, user_data, book_data, login_data, book_data1):
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
#     response = client.delete('/book/del/1', headers=header)
#     assert response.status_code == 200
#
#
# # ------------------------------------------------------------------------------------------------------
# @pytest.mark.abc
# def test_add_cart(client, user_data, login_data, book_data, book_data1, cart_data, update_cart_data):
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
#     response = client.post('/cart/add', json=cart_data, headers=header)  # add the book to the cart items
#     print(response.json())
#     assert response.status_code == 201
#
#     response = client.post('/cart/add', json=update_cart_data, headers=header)
#     assert response.status_code == 201
#
#
# def test_get_cart(client, user_data, login_data, book_data, book_data1, cart_item_data1, update_cart_item_data,cart_item_data):
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
#     response = client.get('/cart/get', headers=header)
#     assert response.status_code == 200
#
#
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
