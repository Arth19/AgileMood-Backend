from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud.crud as crud
import models.user as user_models
import schemas.user as user_schema

from databases.sqlite_data_provider import engine, get_db

user_models.db.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=user_schema.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "Usuário deletado com sucesso"}
