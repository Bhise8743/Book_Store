from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import BigInteger, Integer, String, Column, create_engine, Boolean, ForeignKey

from Core.setting import postgresSQL_password, database_name

engine = create_engine(f'postgresql+psycopg2://postgres:{postgresSQL_password}@localhost:5432/{database_name}')
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(BigInteger, nullable=False)
    password = Column(String(256), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)
    book = relationship('Book', back_populates='user')
    cart = relationship('Cart', back_populates='user')


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='book')
    cart_items=relationship('CartItems',back_populates='book')

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Integer, default=0)
    total_quantity = Column(Integer, default=0)
    is_ordered = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='cart')
    cart_items = relationship('CartItems',back_populates='cart')

class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    book_id = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'), nullable=False,unique=True)
    cart_id = Column(Integer, ForeignKey('cart.id', ondelete='CASCADE'), nullable=False)
    book = relationship('Book', back_populates='cart_items')
    cart = relationship('Cart', back_populates='cart_items')


'''
book 
id  book_name auther price quantity user_id

post and delete put  == > access for super user 

get both super user or normal user
'''
"""
cart
id  total_price (default = 0) total_quantity (default = 0) user_id is_ordered (Boolean default false)    {just like basket in the super market }

add book to cart , remove items , up
"""

"""
cart_items 
id price quantity cart_id (FK)  book_id (FK) 

cart is one book 
"""
