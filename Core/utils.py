
# import the hash algorithm
from passlib.hash import pbkdf2_sha256

def hash_password(raw_password):
    return pbkdf2_sha256.hash(raw_password)

def verify_password(raw_password ,hash_password):
    return pbkdf2_sha256.verify(raw_password ,hash_password)
