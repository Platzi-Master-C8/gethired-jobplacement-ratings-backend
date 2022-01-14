from sqlalchemy.orm import Session

from ratings.models import models
from ratings.schemas import schemas


def get_company_evaluation_by_id(db: Session, id: int):
    return db.query(models.CompanyEvaluation).filter(models.CompanyEvaluation.id == id).first()


def get_company_evaluations_by_company_id(db: Session, company_id: int):
    return db.query(models.CompanyEvaluation).filter(models.CompanyEvaluation.company_id == company_id).all()


def create_company_evaluation(db: Session, company_evaluation: schemas.CompanyEvaluationCreate):
    db_company_evaluation_instance = models.CompanyEvaluation(
        company_id=company_evaluation.company_id,
        job_title=company_evaluation.job_title,
        content_type=company_evaluation.content_type,
        start_date=company_evaluation.start_date,
        end_date=company_evaluation.end_date,
        is_still_working_here=company_evaluation.is_still_working_here,
        applicant_email=company_evaluation.applicant_email,
        career_development_rating=company_evaluation.career_development_rating.value,
        diversity_equal_opportunity_rating=company_evaluation.diversity_equal_opportunity_rating.value,
        working_environment_rating=company_evaluation.working_environment_rating.value,
        salary_rating=company_evaluation.salary_rating.value,
        job_location=company_evaluation.job_location,
        salary=company_evaluation.salary,
        currency_type=company_evaluation.currency_type.value,
        salary_frequency=company_evaluation.salary_frequency.value,
        recommended_a_friend=company_evaluation.recommended_a_friend,
        allows_remote_work=company_evaluation.allows_remote_work,
        is_legally_company=company_evaluation.is_legally_company,
    )
    db.add(db_company_evaluation_instance)
    db.commit()
    db.refresh(db_company_evaluation_instance)
    return db_company_evaluation_instance


def increse_utility_counter(db: Session, id: int):
    company_evaluation = get_company_evaluation_by_id(db=db, id=id)
    company_evaluation.utility_counter = company_evaluation.utility_counter + 1
    db.add(company_evaluation)
    db.commit()
    return company_evaluation

def increse_non_utility_counter(db: Session, id: int):
    company_evaluation = get_company_evaluation_by_id(db=db, id=id)
    company_evaluation.non_utility_counter = company_evaluation.non_utility_counter + 1
    db.add(company_evaluation)
    db.commit()
    return company_evaluation