from sqlalchemy.orm import Session
from app import models

def get_purchases_by_user(db: Session, user_id: int) -> list[models.Purchase]:
    return db.query(models.Purchase).filter(models.Purchase.user_id == user_id).all()

def create_purchase(db: Session, user_id: int, flower_id: int) -> models.Purchase:
    purchase = models.Purchase(user_id=user_id, flower_id=flower_id)
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase

