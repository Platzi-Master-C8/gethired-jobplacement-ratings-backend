# Python
from itertools import count
import os

# Typing
from typing import Dict, List

# Third-party libraries
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import requests

# Dotenv
from dotenv import load_dotenv

# Project
from ratings.models import models
from ratings.schemas import schemas


load_dotenv()
COMPANIES_ENDPOINT = os.getenv("COMPANIES_ENDPOINT")


def check_company_id_exist(company_id: int) -> int:
    """Function to check if a company id exists

    Args:
        company_id (int): ID of the compnay to insert a company evaluation

    Returns:
        if company_id exist in the registers of companies
            return int: The company id
        else company_is not exist
            return int: -1 to indicate non-existence
    """

    r = requests.get(COMPANIES_ENDPOINT)
    companies_response = r.json()["data"]
    list_of_company_ids = [company["id"] for company in companies_response]

    try:
        company_id = list_of_company_ids.index(company_id)
    except:
        company_id = -1

    return company_id


def get_company_evaluation_by_id(db: Session, id: int):
    return (
        db.query(models.CompanyEvaluation)
        .filter(models.CompanyEvaluation.id == id)
        .first()
    )


def get_company_evaluations_by_company_id(db: Session, company_id: int):
    if check_company_id_exist(company_id) != -1:

        try:
            list_of_company_evaluations = (
                db.query(models.CompanyEvaluation)
                .filter(models.CompanyEvaluation.company_id == company_id)
                .all()
            )

            return list_of_company_evaluations

        except SQLAlchemyError as error:
            raise error
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")


def create_company_evaluation(
    db: Session, company_evaluation: schemas.CompanyEvaluationCreate, company_id: int
):
    """Create a new company evaluation

    Args:
        db (Session): SQLAlchemy database session.
        company_evaluation (schemas.CompanyEvaluationCreate): New company evaluation to create.

    Returns:
        [company_evaluation]: Company evaluation created
    """
    if check_company_id_exist(company_id) != -1:

        try:
            company_evaluation = models.CompanyEvaluation(
                company_id=company_id,
                job_title=company_evaluation.job_title.title().strip(),
                content_type=company_evaluation.content_type.capitalize().strip(),
                start_date=company_evaluation.start_date,
                end_date=company_evaluation.end_date,
                is_still_working_here=company_evaluation.is_still_working_here,
                applicant_email=company_evaluation.applicant_email.lower().strip(),
                career_development_rating=company_evaluation.career_development_rating.value,
                diversity_equal_opportunity_rating=company_evaluation.diversity_equal_opportunity_rating.value,
                working_environment_rating=company_evaluation.working_environment_rating.value,
                salary_rating=company_evaluation.salary_rating.value,
                job_location=company_evaluation.job_location.capitalize().strip(),
                salary=company_evaluation.salary,
                currency_type=company_evaluation.currency_type.value,
                salary_frequency=company_evaluation.salary_frequency.value,
                recommended_a_friend=company_evaluation.recommended_a_friend,
                allows_remote_work=company_evaluation.allows_remote_work,
                is_legally_company=company_evaluation.is_legally_company,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            db.add(company_evaluation)
            db.commit()
            db.refresh(company_evaluation)

        except SQLAlchemyError as error:
            raise error
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")

    return company_evaluation


def increse_evaluation_utility_rating(db: Session, company_evaluation_id: int) -> Dict:

    company_evaluation = get_company_evaluation_by_id(db=db, id=company_evaluation_id)
    company_evaluation.utility_counter += 1
    db.add(company_evaluation)
    db.commit()
    return company_evaluation


def increase_evaluation_non_utility_rating(
    db: Session, company_evaluation_id: int
) -> Dict:

    company_evaluation = get_company_evaluation_by_id(db=db, id=company_evaluation_id)
    company_evaluation.non_utility_counter += 1
    db.add(company_evaluation)
    db.commit()

    return company_evaluation


def get_all_reporting_reason_types(db: Session) -> List[Dict]:
    return db.query(models.ReportingReasonType).all()


def get_reporting_reason_by_id(db: Session, reporting_reason_type_id: int) -> Dict:
    return (
        db.query(models.ReportingReasonType)
        .filter(models.ReportingReasonType.id == reporting_reason_type_id)
        .first()
    )


def create_complaint(
    db: Session, complaint_body: schemas.ComplaintCreate, company_evaluation_id: int
) -> dict:
    """Create a complaint for a company evaluation

    Args:
        db (Session): Instance of the database which all us manage and persist operation in the ORM
        complaint_body (schemas.complaintCreate): Request body to create a complaint using pydantic models
        company_evaluation_id (int): The id of the company evaluation to attach a complaint

    Returns:
        complaint: Complaint made to the company's evaluation
    """

    try:
        company_evaluation = get_company_evaluation_by_id(
            db=db, id=company_evaluation_id
        )

        complaint = models.Complaint(
            reporting_reason_type_id=complaint_body.reporting_reason_type_id,
            problem_description=complaint_body.problem_description,
            email=complaint_body.email.lower(),
        )

        company_evaluation.complaints.append(complaint)
        db.add(complaint)
        db.commit()
        db.refresh(complaint)

    except SQLAlchemyError as error:
        raise error

    return complaint
