"""

@Author: Omkar Bhise

@Date: 2024-01-22 11:30:00

@Last Modified by: Omkar Bhise

@Last Modified time: 2024-01-29 11:30:00

@Title :  User Registration

"""
from fastapi import FastAPI,Security,Depends
from fastapi.security import APIKeyHeader
from Core.utils import jwt_authentication
from routes.user import user
from routes.book import book
from routes.cart import cart
app = FastAPI()
app.include_router(user,prefix='/user')
app.include_router(book, prefix='/book',
                   dependencies=[Security(APIKeyHeader(name='authorization')), Depends(jwt_authentication)])
app.include_router(cart,prefix='/cart',dependencies=[Security(APIKeyHeader(name='authorization')), Depends(jwt_authentication)])