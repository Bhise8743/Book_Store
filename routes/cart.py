import random

from fastapi import APIRouter, status, Response, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import CartItemsSchema
from model import get_db, Cart, Book, CartItems, User
from task import email_notification

cart = APIRouter()


@cart.post('/add', status_code=status.HTTP_201_CREATED, tags=["Cart"])
def add_book_to_cart(body: CartItemsSchema, response: Response, request: Request, db: Session = Depends(get_db)):
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            cart_data = Cart(user_id=request.state.user.id)
            db.add(cart_data)
        book_data = db.query(Book).filter_by(id=body.book_id).one_or_none()
        if book_data is None:
            raise HTTPException(detail="This book is not present ", status_code=status.HTTP_400_BAD_REQUEST)
        if body.quantity > book_data.quantity:
            raise HTTPException(detail=f"This book is present and there Quantity is {book_data.quantity}",
                                status_code=status.HTTP_400_BAD_REQUEST)

        books_price = body.quantity * book_data.price
        cart_items_data = db.query(CartItems).filter_by(book_id=body.book_id).one_or_none()
        if cart_items_data is None:
            cart_items_data = CartItems(price=books_price, quantity=body.quantity, book_id=book_data.id,
                                        cart_id=cart_data.id)
            db.add(cart_items_data)
        else:
            cart_data.total_price -= cart_items_data.price
            cart_data.total_quantity -= cart_items_data.quantity

        cart_data.total_price += books_price
        cart_data.total_quantity += body.quantity
        db.commit()
        db.refresh(cart_data)
        db.refresh(cart_items_data)
        return {'message': 'Book added on cart Successfully', 'status': 201}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}

@cart.get('/get', status_code=status.HTTP_200_OK, tags=["Cart"])
def get_cart_details(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail='This cart is not present ', status_code=status.HTTP_400_BAD_REQUEST)
        if cart_data.total_quantity == 0:
            raise HTTPException(detail="The cart is empty", status_code=status.HTTP_400_BAD_REQUEST)
        return {'message': "Card Data found Successfully", 'status': 200, 'data': cart_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@cart.get('/get/{cart_id}', status_code=status.HTTP_200_OK, tags=["Cart"])
def get_all_cart_items_details(card_id: int, request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        cart_data = db.query(Cart).filter_by(id=card_id, user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail='Cart is empty', status_code=status.HTTP_400_BAD_REQUEST)

        card_items_data = db.query(CartItems).filter_by(cart_id=card_id).all()
        return {'message': 'All cart items get successfully ', 'status': 200, 'data': card_items_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@cart.get('/conform', status_code=status.HTTP_200_OK, tags=["Cart"])
def confirm_order(response: Response, request: Request, db: Session = Depends(get_db)):
    try:
        cart_data = db.query(Cart).filter_by(user_id=request.state.user.id).one_or_none()
        if cart_data is None:
            raise HTTPException(detail='The Cart is Empty', status_code=status.HTTP_400_BAD_REQUEST)
        cart_items_details = db.query(CartItems).filter_by(cart_id=cart_data.id).all()

        message = f"""
                Thank you for conforming the order 
                Items Details is :
                {cart_items_details}
                Total Quantity : {cart_data.total_quantity}
                Total Price is : {cart_data.total_price}    
            """
        cart_data.is_ordered = True
        user_data = db.query(User).filter_by(id=request.state.user.id).one_or_none()
        email_notification.delay(user_data.email, message, 'Order Conformation')
        db.commit()
        return {'message': 'Order Conformation Successfully', 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
