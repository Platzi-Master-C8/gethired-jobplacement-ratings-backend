from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Path, Body, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ratings.routes import example_root

from ratings.cruds import crud
from ratings.models import models
from ratings.schemas import schemas

from ratings.config.database import SessionLocal, engine

# Create the database tables
models.Base.metadata.create_all(engine)


app = FastAPI(title="Jobplacement - Ratings API")

# Dependency with database connection


def get_database_session():
    session_local_db = SessionLocal()
    try:
        yield session_local_db
    finally:
        session_local_db.close()


@app.post(
    path="/companyEvaluations/",
    response_model=schemas.CompanyEvaluationOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Company Evaluations"],
    summary="Create a new Company Evaluation"
)
def create_company_evaluation(
        company_evaluation: schemas.CompanyEvaluationCreate = Body(...),
        session_local_db: Session = Depends(get_database_session)
):
    """ 
        # Create a Company Evaluation

        This Path Operation create a company evaluation and save the information in the database.

        ## Parameters:
        - Request body parameter:
            - **company_id: int** (required) The id of the company to which this assessment belongs.
            - **job_title: str** (required) -> The name of the position you have or had in the company.
            - **content_type: str** (required) -> The content of the evaluation to be added to the company's.
            - **start_date: date** (required) -> The date on which the person started working with the company.
            - **end_date:date** (optional) -> The date on which the person finished working with the company.
            - **is_still_working_here: int** (optional) -> The date on which the person finished working with the company.
            - **applicant_email: EmailStr** (required) -> The id of the company to which this assessment belongs
            - **career_development_rating:CompanyRatingType** (required) -> It represents the rating with which the career development will be rated.
            - **diversity_equal_opportunity_rating: CompanyRatingType** (required) -> Represents the rating with which the diversity and equal opportunity will be rated.
            - **working_environment_rating: CompanyRatingType** (required) -> Represents the rating with which the work environment within the company will be rate.
            - **salary_rating: CompanyRatingType** (required) ->Represents the salary with which the work environment within the company will be rate.
            - **job_location: str** (required) -> Location of the work site.
            - **salary: decimal(12,2)** (required) -> The salary the person earned in this job.
            - **currency_type: CurrencyCodeISO4217** (required) -> The type of currency in which the company is paid.
            - **salary_frequency: SalaryFrecuency** (required) -> The type of currency in which the company is paid.
            - **recommended_a_friend: int** (required) -> The type of currency in which the company is paid.
            - **recommended_a_friend: int** (required) -> The type of currency in which the company is paid.
            - **is_legally_company: int** (required) -> The type of currency in which the company is paid.


        ## Returns:
        - A dictionary with company_id, job_title, content_type, start_date, end_date,is_still_working_here,utility_counter, non_utility_counter 
    """
    return crud.create_company_evaluation(db=session_local_db, company_evaluation=company_evaluation)


@app.get(
    path="/companies/{company_id}/companyEvaluations/",
    response_model=Page[schemas.CompanyEvaluationOut],
    status_code=status.HTTP_200_OK,
    tags=["Company Evaluations"],
    summary="Obtain all the company evaluations by the id of the company"
)
def get_company_evaluations_by_company_id(

    company_id: int = Path(
        ...,
        gt=0,
        title="Company id",
        example=1,
        description="This is the company id."
    ),
    session_local_db: Session = Depends(get_database_session)
):
    company_evaluations = crud.get_company_evaluations_by_company_id(
        session_local_db,
        company_id=company_id
    )
    return paginate(company_evaluations)


add_pagination(app)


@app.patch(
    path="/companyEvaluations/{id}/increaseUtilityRating/",
    response_model=schemas.CompanyEvaluationOut,
    status_code=status.HTTP_200_OK,
    tags=["Company Evaluations"],
    summary="Increase in one point the utility of one company evaluation."
)
def increse_evaluation_utility_rating(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(
        ...,
        gt=0,
        example=1,
        title="This is the id of the company Evaluation",
        description="This is the id of the company evaluation"
    )
):
    company_evaluation = crud.get_company_evaluation_by_id(
        db=session_local_db, id=id)
    if company_evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Company Evaluation not found"
        )
    return crud.increse_evaluation_utility_rating(db=session_local_db, company_evaluation_id=id)


@app.patch(
    path="/companyEvaluations/{id}/increaseNonUtilityRating/",
    response_model=schemas.CompanyEvaluationOut,
    status_code=status.HTTP_200_OK,
    tags=["Company Evaluations"],
    summary="Increase in one point the non-utility of one company evaluation."
)
def increse_evaluation_non_utility_rating(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(
        ...,
        gt=0,
        example=1,
        title="This is the id of the company Evaluation",
        description="This is the id of the company evaluation"
    )
):
    company_evaluation = crud.get_company_evaluation_by_id(
        db=session_local_db, id=id)
    if company_evaluation is None:
        raise HTTPException(
            status_code=404,
            detail="Company Evaluation not found"
        )
    return crud.increase_evaluation_non_utility_rating(db=session_local_db, company_evaluation_id=id)
