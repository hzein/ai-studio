# Hashing
import bcrypt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from sql_db import crud
from config import SECRET_KEY, ALGORITHM


def get_password_hash(password):
    # return pwd_context.hash(password)
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password):
    # return pwd_context.verify(plain_password, hashed_password)
    password_byte_enc = plain_password.encode("utf-8")
    # hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def get_user(username: str, db: Session):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user:
        return db_user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
