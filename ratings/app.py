from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from ratings.routes import example_root

from ratings.models import models
from ratings.schemas import schemas
from ratings.cruds import crud

from ratings.config.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(engine)


app = FastAPI(title="Jobplacement - Ratings API")
app.include_router(example_root)


# Dependency with database conecction
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
