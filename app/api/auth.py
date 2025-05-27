from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db import get_db
from app.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup", status_code=200)
async def signup(
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    photo: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    user_exist = crud.users.get_user_by_email(db, email)
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")

    photo_bytes = await photo.read() if photo else None

    user_in = schemas.UserCreate(
        email=email,
        full_name=full_name,
        password=password,
        photo=photo_bytes
    )
    crud.users.create_user(db, user_in)
    return {"message": "User created successfully"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

