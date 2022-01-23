# Python

# Typing
from typing import Dict, List

# SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


# Project
from ratings.models import models
from ratings.schemas import schemas


def get_company_evaluation_by_id(db: Session, id: int):
    return (
        db.query(models.CompanyEvaluation)
        .filter(models.CompanyEvaluation.id == id)
        .first()
    )


def get_company_evaluations_by_company_id(db: Session, company_id: int):
    return (
        db.query(models.CompanyEvaluation)
        .filter(models.CompanyEvaluation.company_id == company_id)
        .all()
    )


def create_company_evaluation(
    db: Session, company_evaluation: schemas.CompanyEvaluationCreate
):
    """Create a new company evaluation

    Args:
        db (Session): SQLAlchemy database session.
        company_evaluation (schemas.CompanyEvaluationCreate): New company evaluation to create.

    Returns:
        [company_evaluation]: Company evaluation created
    """
    try:
        company_evaluation = models.CompanyEvaluation(
            company_id=company_evaluation.company_id,
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
