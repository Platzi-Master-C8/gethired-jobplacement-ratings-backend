from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Body
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


# Dependency with database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(path="/companyEvaluations/{id}", response_model=schemas.CompanyEvaluation, status_code=status.HTTP_200_OK)
def get_company_evaluations_by_id(

    db: Session = Depends(get_db),
    id: int = Path(
        ...,
        gt=0,
        title="Company evaluation id",
        description="This is the company evaluation id."
    )
):
    company_evaluation = crud.get_company_evaluation_by_id(db, id=id)
    if company_evaluation is None:
        raise HTTPException(
            status_code=404, detail="Company evaluation not found")
    return company_evaluation


@app.get("/companyEvaluations/company/{company_id}", response_model=List[schemas.CompanyEvaluation], status_code=status.HTTP_200_OK)
def get_company_evaluations_by_company_id(
    db: Session = Depends(get_db),
    company_id: int = Path(
        ...,
        gt=0,
        title="Company id",
        description="This is the company id."
    )
):
    company_evaluations = crud.get_company_evaluations_by_company_id(
        db,
        company_id=company_id
    )
    return company_evaluations


@app.post("/companyEvaluations/", response_model=schemas.CompanyEvaluation, status_code=status.HTTP_201_CREATED)
def create_company_evaluation(
        company_evaluation: schemas.CompanyEvaluationCreate = Body(...),
        db: Session = Depends(get_db)
):
    return crud.create_company_evaluation(db=db, company_evaluation=company_evaluation)
