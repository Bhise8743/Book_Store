import pytz
from fastapi import HTTPException, status, Request, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from model import get_db, User
# import the hash algorithm
from passlib.hash import pbkdf2_sha256
from Core.setting import jwt_algo, secret_key
from datetime import datetime, timedelta


def hash_password(raw_password):
    return pbkdf2_sha256.hash(raw_password)


def verify_password(raw_password, hash_password):
    return pbkdf2_sha256.verify(raw_password, hash_password)


class JWT:
    @staticmethod
    def data_encoding(data: dict):
        if 'exp' not in data:
            expire = datetime.now(pytz.utc) + timedelta(minutes=30)
            data.update({'exp': expire})
        return jwt.encode(data, secret_key, algorithm=jwt_algo)

    @staticmethod
    def data_decoding(token):
        try:
            return jwt.decode(token, secret_key, algorithms=jwt_algo)
        except JWTError as ex:
            raise HTTPException(detail=str(ex), status_code=status.HTTP_400_BAD_REQUEST)


def jwt_authentication(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get('authorization')
    decoded_token = JWT.data_decoding(token)
    user_id = decoded_token.get('user_id')
    user = db.query(User).filter_by(id=user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    request.state.user = user
