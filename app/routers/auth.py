from datetime import timedelta
from jose import JWTError, jwt
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sql_db.database import SessionLocal
from sql_db.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from dependencies import authenticate_user, get_user, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])

oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class User(BaseModel):
    username: str
    email: str
    is_active: bool = True
    role: str


class UserInDb(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
db_dependency = Annotated[Session, Depends(get_db)]


async def get_current_user(
    token: Annotated[str, Depends(oath2_scheme)], db: db_dependency
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: UserInDb = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_admin_user(current_user: UserInDb = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="User is not an admin")
    return current_user


@router.post("/token", response_model=Token)
async def loging_for_access_token(
    from_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(
        username=from_data.username, password=from_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
