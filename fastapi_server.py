from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User, Product, Order, CurrentPrice
from typing import List
from pydantic_models import *

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Вспомогательная функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получить список всех продуктов
@app.get("/products", response_model=List[ProductOut])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# Создать новый продукт
@app.post("/products", response_model=ProductOut)
def create_product(product: ProductIn, db: Session = Depends(get_db)):
    # Преобразовать входную Pydantic-модель в ORM-модель и добавить в базу данных
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Получить информацию о продукте по id
@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#обновить информацию о продукте
@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated_product: ProductIn, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated_product.dict().items():
        if value is not None:
            setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@app.post("/products/{product_id}/purchase", response_model=bool)
def purchase_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity <= 0:
        return False

    product.quantity -= 1
    db.commit()
    db.refresh(product)
    return True


@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.dict().items():
        if value is not None:
            setattr(product, key, value)

    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product


@app.post("/ton_prices", response_model=CpriceOut)
def create_current_price(product: CpriceIn, db: Session = Depends(get_db)):
    # Преобразовать входную Pydantic-модель в ORM-модель и добавить в базу данных
    db_current_price = Product(**product.dict())
    db.add(db_current_price)
    db.commit()
    db.refresh(db_current_price)
    return db_current_price


@app.get("/ton_prices", response_model=List[CpriceOut])
def get_current_prices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    prices = db.query(CurrentPrice).offset(skip).limit(limit).all()
    return prices
