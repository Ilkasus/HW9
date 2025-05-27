from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    photo: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True



class FlowerBase(BaseModel):
    name: str
    quantity: int
    price: float

class FlowerCreate(FlowerBase):
    pass

class FlowerOut(FlowerBase):
    id: int

    class Config:
        orm_mode = True



class PurchaseOut(BaseModel):
    id: int
    user_id: int
    flower_id: int

    class Config:
        orm_mode = True

