from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schema import UserSchema, LoginSchema
from model import get_db, User, Cart
from Core.utils import verify_password, hash_password, JWT
from Core.setting import super_key
from task import email_notification

user = APIRouter()


@user.post("/register", status_code=status.HTTP_201_CREATED, tags=["User"])
async def add_user(body: UserSchema, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function is used to takes the user information from user and add on Database
        Parameter: user : UserSchema  => Schema of the user
                        response : Response  it response to the user
                        db: Session = Depends on the get_db  i.e. he yield the database
        Return: JSON form dict in that mess:
        data = body.model_dump()
        data['password'] = hash_password(data['password'])
        user_super_key = data['super_key']
        if user_super_key == super_key:  # key is in the form of string
            print("yes")
            data.update({'is_super_user': True})
        data.pop('super_key')
        user_data = User(**data)
        db.add(user_data)
        db.commit()
        db.refresh(user_data)

        token = JWT.data_encoding({'user_id': user_data.id})
        verification_link = f'http://127.0.0.1:8080/user/verify?token={token}'
        email_notification.delay(user_data.email, verification_link, 'Email Verification')

        return {'message': "User Registration Successfully ", 'status': 201, 'data': user_data}
    except IntegrityError as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Username or Email is already exist', 'status': 400}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@user.post('/login', status_code=status.HTTP_200_OK, tags=["User"])
def user_login(body: LoginSchema, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function is used to take the login credentials from the user and verify them
        Parameter: body : LoginSchema  => Schema of the login
                   response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. he yield the database
        Return: message and status code in JSON format
    """
    try:
        user_data = db.query(User).filter_by(user_name=body.user_name).one_or_none()
        if not user_data:
            raise HTTPException(detail="Invalid Username", status_code=status.HTTP_400_BAD_REQUEST)
        if not verify_password(body.password, user_data.password):
            raise HTTPException(detail="Invalid Password", status_code=status.HTTP_400_BAD_REQUEST)
        # if not user_data.is_verified:
        #     raise HTTPException(detail="Email is Not Verified", status_code=status.HTTP_400_BAD_REQUEST)

        token = JWT.data_encoding({'user_id': user_data.id})
        return {'message': "Login successfully ", 'status': 200, 'access_token': token}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@user.get('/verify', status_code=status.HTTP_200_OK, tags=["User"])
def email_verification(token: str, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function is used to verify the user email
        Parameter: response : Response  it response to the user
                   db: Session = Depends on the get_db  i.e. he yield the database
        Return: JSON form dict in that message, status code, data
    """
    try:
        decoded_data = JWT.data_decoding(token)
        user_id = decoded_data.get('user_id')
        user_data = db.query(User).filter_by(id=user_id).one_or_none()
        if user_data is None:
            raise HTTPException(detail="User is Not Present", status_code=status.HTTP_400_BAD_REQUEST)
        user_data.is_verified = True
        db.commit()
        return {'message': "Email Verified Successfully", 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@user.put('/forget/{email}', status_code=status.HTTP_200_OK, tags=["User"])
def forget_username_password(email: str, body: LoginSchema, response: Response, db: Session = Depends(get_db)):
    try:
        user_data = db.query(User).filter_by(email=email).one_or_none()
        if user_data is None:
            raise HTTPException(detail="This user is not present ", status_code=status.HTTP_400_BAD_REQUEST)
        if not user_data.is_verified:
            raise HTTPException(detail='You are not a verified user', status_code=status.HTTP_400_BAD_REQUEST)
        data = body.model_dump()
        data['password'] = hash_password(data['password'])
        [setattr(user_data, key, value) for key, value in data.items()]
        db.commit()
        db.refresh(user_data)
        return {'message': 'Successfully updated Username or Password', 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@user.patch('/change_email/{email}', status_code=status.HTTP_200_OK, tags=["User"])
def change_email(email: str, body: LoginSchema, response: Response, db: Session = Depends(get_db)):
    try:
        user_data = db.query(User).filter_by(user_name=body.user_name).one_or_none()
        if not user_data:
            raise HTTPException(detail="This is not valid username", status_code=status.HTTP_400_BAD_REQUEST)
        if not verify_password(body.password, user_data.password):
            raise HTTPException(detail='Password is Not valid ', status_code=status.HTTP_400_BAD_REQUEST)
        if not user_data.is_verified:
            raise HTTPException(detail="You are not verified user ", status_code=status.HTTP_400_BAD_REQUEST)
        user_data['email'] = email
        user_data.is_verified = False
        print("HHII")
        db.commit()

        token = JWT.data_encoding({'user_id': user_data.id})
        verification_link = f'http://127.0.0.1:8080/user/verify?token={token}'
        email_notification.delay(user_data.email, verification_link, 'Email Verification')

        return {'message': 'Email is Changed Successfully', 'status': 200}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}




# @user.get('/order_verify', status_code=status.HTTP_200_OK, tags=["User"])
# def order_conformation_verification(token: str, response: Response, db: Session = Depends(get_db)):
#     try:
#         decoded_data = JWT.data_decoding(token)
#         user_id = decoded_data.get('user_id')
#         cart_data = db.query(Cart).filter_by(user_id=user_id).one_or_none()
#         cart_data.is_ordered = True
#         db.commit()
#         return {'Message': "Order Conformed successfully", 'status': 200}
#     except Exception as ex:
#         response.status_code = status.HTTP_400_BAD_REQUEST
#         return {'message': str(ex), 'status': 400}

