from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db
from app.auth import get_current_user
import json

router = APIRouter()

CART_COOKIE_NAME = "cart_items"

@router.post("/purchased", status_code=200)
def purchase_items(
    request: Request,
    response: Response,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart_cookie = request.cookies.get(CART_COOKIE_NAME)
    if not cart_cookie:
        raise HTTPException(status_code=400, detail="Cart is empty")

    flower_ids = json.loads(cart_cookie)
    if not flower_ids:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for flower_id in flower_ids:
        crud.purchases.create_purchase(db, current_user.id, flower_id)

    response.delete_cookie(CART_COOKIE_NAME)
    return {"message": "Purchase successful"}

@router.get("/purchased", response_model=list[schemas.Flower])
def get_purchased_items(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    purchases = crud.purchases.get_purchases_by_user(db, current_user.id)
    flowers = [purchase.flower for purchase in purchases]
    return flowers

