from fastapi import APIRouter, Depends, Request, Response, Form
from app import crud, schemas
from sqlalchemy.orm import Session
from app.db import get_db

import json

router = APIRouter()

CART_COOKIE_NAME = "cart_items"

@router.post("/cart/items")
def add_to_cart(
    flower_id: int = Form(...),
    request: Request = None,
    response: Response = None
):
    cart_cookie = request.cookies.get(CART_COOKIE_NAME)
    if cart_cookie:
        cart = json.loads(cart_cookie)
    else:
        cart = []

    cart.append(flower_id)

    response.set_cookie(key=CART_COOKIE_NAME, value=json.dumps(cart), httponly=True)
    return {"message": "Flower added to cart"}

@router.get("/cart/items", response_model=schemas.CartResponse)
def get_cart_items(request: Request, db: Session = Depends(get_db)):
    cart_cookie = request.cookies.get(CART_COOKIE_NAME)
    if not cart_cookie:
        return {"items": [], "total": 0}

    flower_ids = json.loads(cart_cookie)
    flowers = db.query(crud.models.Flower).filter(crud.models.Flower.id.in_(flower_ids)).all()

    total = sum(flower.price for flower in flowers)

    items = [
        {"id": flower.id, "name": flower.name, "price": flower.price}
        for flower in flowers
    ]
    return {"items": items, "total": total}

