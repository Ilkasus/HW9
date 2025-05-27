from fastapi import FastAPI
from app.db.base import engine, Base
from app.api import auth, users, flowers, cart, purchases

app = FastAPI(title="Flower Marketplace API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(flowers.router, prefix="/flowers", tags=["flowers"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(purchases.router, prefix="/purchased", tags=["purchased"])

@app.get("/")
def root():
    return {"message": "Welcome to the Flower Marketplace API"}

