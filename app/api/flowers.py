from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db

router = APIRouter()

@router.get("/flowers", response_model=list[schemas.Flower])
def list_flowers(db: Session = Depends(get_db)):
    flowers = crud.flowers.get_flowers(db)
    return flowers

@router.post("/flowers", response_model=int, status_code=201)
def create_flower(flower: schemas.FlowerCreate, db: Session = Depends(get_db)):
    new_flower = crud.flowers.create_flower(db, flower)
    return new_flower.id

@router.patch("/flowers/{flower_id}", response_model=schemas.Flower)
def update_flower(flower_id: int = Path(...), flower: schemas.FlowerCreate = Depends(), db: Session = Depends(get_db)):
    updated_flower = crud.flowers.update_flower(db, flower_id, flower)
    if not updated_flower:
        raise HTTPException(status_code=404, detail="Flower not found")
    return updated_flower

@router.delete("/flowers/{flower_id}", status_code=204)
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    success = crud.flowers.delete_flower(db, flower_id)
    if not success:
        raise HTTPException(status_code=404, detail="Flower not found")
    return None

