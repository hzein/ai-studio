from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from sql_db.database import SessionLocal
from sql_db import crud, schemas
from routers.auth import check_admin_user

router = APIRouter(prefix="/users", tags=["users"])


class User(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserInDb(User):
    hashed_password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
db_dependency = Annotated[Session, Depends(get_db)]
admin_dependency = Annotated[dict, Depends(check_admin_user)]


# Create User
@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: db_dependency, admin: admin_dependency):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# Get All Users
@router.get("/", response_model=list[schemas.User])
def read_users(
    db: db_dependency, admin: admin_dependency, skip: int = 0, limit: int = 100
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Get a User
@router.get("/{user_id}", response_model=schemas.User)
def read_user(db: db_dependency, admin: admin_dependency, user_id: int):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
