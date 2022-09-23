from fastapi import Depends, FastAPI
from database import SessionLocal, engine, get_db
import models, schemas, oauth, crud
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from routers import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)


# loginする時はFormでの入力を要求し、Tokenを発行して返す
# クライアントはTokenを持っておき、毎回Headerに含めてリクエストする
# 以降はtokenを確認するためにoauth2_schemeを使用
@app.post("/token", response_model=schemas.Token, tags=['Oauthentication'])
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(form_data.username, db)
    access_token = oauth.create_access_token({"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", response_model=schemas.UserOut)
async def get_user_me(user: schemas.UserOut = Depends(oauth.get_current_user)):
    return user

