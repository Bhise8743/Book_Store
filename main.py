"""

@Author: Omkar Bhise

@Date: 2024-01-22 11:30:00

@Last Modified by: Omkar Bhise

@Last Modified time: 2024-01-23 02:30:00

@Title :  User Registration

"""
from fastapi import FastAPI

from routes.user import user

app = FastAPI()
app.include_router(user,prefix='/user')