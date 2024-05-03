from sqlalchemy.orm import Session

from . import models, schemas
import os

print(os.getcwd())
from dependencies import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        role=user.role,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_prompts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prompts).offset(skip).limit(limit).all()


def prompt_create(db: Session, prompt: schemas.PromptCreate, user_id: int):
    db_prompt = models.Prompts(**prompt.model_dump(), owner_id=user_id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt
