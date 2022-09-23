from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from database import get_db
import schemas, models
import crud, oauth

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/create", response_model=schemas.UserOut)
async def create_user(
    username: str = Form(),
    email: EmailStr = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    created_user = crud.create_user(username, email, password, db)
    return created_user


@router.get("/", response_model=list[schemas.UserOut])
async def get_users(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, offset, limit)

@router.get("/{email}", response_model=schemas.UserOut)
async def get_user(email: EmailStr, db: Session = Depends(get_db)):
    return crud.get_user_by_email(email, db)

@router.put("/update", response_model=schemas.UserOut)
async def update_user(
    new_user: schemas.UserIn,
    current_user: schemas.UserOut = Depends(oauth.get_current_user),
    db: Session = Depends(get_db),
):
    return crud.update_user(current_user, new_user.username, new_user.email, new_user.password, db)

@router.delete("/delete")
async def delete_user(current_user: schemas.UserOut = Depends(oauth.get_current_user), db: Session = Depends(get_db)):
    return crud.delete_user(current_user, db)