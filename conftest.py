from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from model import get_db, Base

engine = create_engine(f'postgresql+psycopg2://postgres:12345@localhost:5432/Test_Book_Store')
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
@pytest.fixture
def user_data():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise8635@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra",
        "super_key": "99604017"
    }

@pytest.fixture
def user_data_error():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise8635@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra"
    }

@pytest.fixture
def user_data_not_super_user():
    return {
        "user_name": "Omkar@1234",
        "password": "Omkar@1234",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise874386@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra"
    }

@pytest.fixture
def login_data():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123"
    }
@pytest.fixture
def login_data1():
    return {
        "user_name": "Omkar@1234",
        "password": "Omkar@1234"
    }

@pytest.fixture
def book_data():
    return {
        "book_name": "Python",
        "author": "Balguru Swami",
        "price": 200,
        "quantity": 10
    }

@pytest.fixture
def book_data_error():
    return {
        "book_name": 23,  #422 Unprocessable Entity
        "author": "Balguru Swami",
        "price": "200",      # data types error
        "quantity": 10
    }

@pytest.fixture
def book_data1():
    return {
        "book_name": "Java",
        "author": "Balguru Swami",
        "price": 250,
        "quantity": 10
    }


@pytest.fixture
def cart_item_data():
    return {
        "book_id": 1,
        "quantity": 5
    }


@pytest.fixture
def update_cart_item_data():
    return {
        "book_id": 1,
        "quantity": 7
    }


@pytest.fixture
def cart_item_data1():
    return {
        "book_id": 2,
        "quantity": 5
    }

@pytest.fixture
def cart_item_data2():
    return {
        "book_id": 3,
        "quantity": 2
    }