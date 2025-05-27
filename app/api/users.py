from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db
from app.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=schemas.User)
def read_profile(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.users.get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

