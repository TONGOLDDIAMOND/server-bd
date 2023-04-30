from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    subscription_key: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    id: int
    name: str
    subscription_key: str
    price: float
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProductIn(BaseModel):
    name: str
    subscription_key: str
    price: float
    quantity: int

class CpriceIn(BaseModel):
    id: int
    current_price: float
    updated_at: datetime


class CpriceOut(BaseModel):
    current_price: Optional[float]

# class ProductIn(BaseModel):
#     name: Optional[str]
#     subscription_key: Optional[str]
#     price: Optional[float]
#     quantity: Optional[int]
#
#     class Config:
#         orm_mode = True
