import os

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD API")

# Optional CORS support (useful for browser apps)
# Set CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:5173" etc.
cors_origins = os.getenv("CORS_ORIGINS", "")
if cors_origins.strip():
    allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
else:
    # Dev-friendly default; set CORS_ORIGINS to lock this down
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"name": "CRUD API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

# GET /items - list items
@app.get("/items", response_model=list[schemas.Item])
def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination params")
    # prevent accidental huge responses
    limit = min(limit, 500)
    return crud.get_items(db, skip=skip, limit=limit)

# GET /items/{id} - get single item
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# PUT /items/{id} - replace item (full update)
@app.put("/items/{item_id}", response_model=schemas.Item)
def replace_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.replace_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# PATCH /items/{id} - update item (partial update)
@app.patch("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# DELETE /items/{id} - delete item
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# Routes
@app.post("/items", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

#Runs when python main.py is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
