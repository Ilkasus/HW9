from sqlalchemy.orm import Session
from app import models, schemas

def get_flowers(db: Session, skip: int = 0, limit: int = 100) -> list[models.Flower]:
    return db.query(models.Flower).offset(skip).limit(limit).all()

def get_flower(db: Session, flower_id: int) -> models.Flower | None:
    return db.query(models.Flower).filter(models.Flower.id == flower_id).first()

def create_flower(db: Session, flower_create: schemas.FlowerCreate) -> models.Flower:
    db_flower = models.Flower(
        name=flower_create.name,
        quantity=flower_create.quantity,
        price=flower_create.price
    )
    db.add(db_flower)
    db.commit()
    db.refresh(db_flower)
    return db_flower

def update_flower(db: Session, flower_id: int, flower_update: schemas.FlowerCreate) -> models.Flower | None:
    flower = get_flower(db, flower_id)
    if not flower:
        return None
    flower.name = flower_update.name
    flower.quantity = flower_update.quantity
    flower.price = flower_update.price
    db.commit()
    db.refresh(flower)
    return flower

def delete_flower(db: Session, flower_id: int) -> bool:
    flower = get_flower(db, flower_id)
    if not flower:
        return False
    db.delete(flower)
    db.commit()
    return True

