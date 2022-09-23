from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
import models, schemas
import oauth


def get_user_by_email(email: str, db: Session)->schemas.UserOut:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with the email:{email} is not found",
        )
    return user

def create_user(username: str, email: EmailStr, password: str, db: Session):
    new_user = schemas.UserInDB(username=username, email=email, hashed_password=oauth.pwd_context.hash(password))
    user_db = models.User(**new_user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    res = get_user_by_email(email, db)
    return res

def get_users(db: Session, offset: int, limit: int):
    users = db.query(models.User).offset(offset).limit(limit).all()
    return users

def update_user(current_user: schemas.UserOut, username: str, email: EmailStr, password: str, db: Session):
    updated_user = schemas.UserInDB(username=username, email=email, hashed_password=oauth.pwd_context.hash(password))
    db.query(models.User).filter(models.User.email == current_user.email).update(updated_user.dict())
    db.commit()
    res = get_user_by_email(email, db)
    return res

def delete_user(current_user: schemas.UserOut, db: Session):
    db.query(models.User).filter(models.User.email == current_user.email).delete()
    db.commit()
    return {"message": "deleted"}