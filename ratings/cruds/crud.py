# Python
import os
import functools
import operator

# Typing
from typing import Dict, List, Optional

# Third-party libraries
from fastapi import HTTPException
from datetime import datetime
from pydantic import EmailStr, HttpUrl
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import asc, desc
from sqlalchemy import or_
from sqlalchemy import and_
import requests

# Dotenv
from dotenv import load_dotenv

# Project
from ratings.models import models
from ratings.schemas import schemas
from ratings.utils.utils import Util


load_dotenv()
COMPANIES_ENDPOINT = os.getenv("COMPANIES_ENDPOINT")
VACANCIES_ENDPOINT = os.getenv("VACANCIES_ENDPOINT")
AMOUNT_OF_COMPANY_CRITERIA = int(os.getenv("AMOUNT_OF_COMPANY_CRITERIA"))


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


def check_vacancy_id_exist(vacancy_id: int) -> int:
    """Function to check if a vacancy id exists

    Args:
        vacancy (int): ID of the compnay to insert a company evaluation

    Returns:
        if vacancy_id exist in the registers of companies
            return int: The company id
        else vacancy_is not exist
            return int: -1 to indicate non-existence
    """

    r = requests.get(VACANCIES_ENDPOINT)
    vacancies_response = r.json()["data"]
    list_of_company_ids = [vacancy["id"] for vacancy in vacancies_response]

    try:
        company_id = list_of_company_ids.index(vacancy_id)
    except:
        company_id = -1

    return company_id


def get_company_by_id(company_id: int):

    if check_company_id_exist(company_id=company_id) != -1:

        request = requests.get(f"{COMPANIES_ENDPOINT}/{company_id}")
        return request.json()["data"]
    else:
        return None


def create_vacancy_applicant(vacancy_id: int, applicant_id):

    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "vacancy_id": vacancy_id,
        "applicant_id": applicant_id,
    }

    response = requests.post(
        f"{VACANCIES_ENDPOINT}/{vacancy_id}/applications", json=data, headers=headers
    )
    print("Status Code", response.status_code)
    print("----------------")
    print("JSON Response ", response.json())


def get_vacancy_by_id(vacancy_id: int) -> dict:

    r = requests.get(VACANCIES_ENDPOINT)
    vacancies_response = r.json()["data"]
    vacancy = [vacancy for vacancy in vacancies_response if vacancy["id"] == vacancy_id]

    if vacancy == []:
        raise HTTPException(status_code=404, detail="Vacancy Not Found")

    return vacancy[0]


def get_company_evaluation_by_id(db: Session, id: int):
    return (
        db.query(models.CompanyEvaluation)
        .filter(models.CompanyEvaluation.id == id)
        .first()
    )


def get_applicant_by_id(db: Session, id: int):
    try:
        applicant = db.query(models.Applicant).filter(models.Applicant.id == id).first()
        if applicant != None:
            return applicant
        else:
            raise HTTPException(status_code=404, detail="Applicant Not Found")
    except SQLAlchemyError as error:
        raise error


def get_amount_of_company_evaluation_by_id(db: Session, company_id: int):
    try:
        amount_of_company_evaluation_by_company_id = (
            db.query(models.CompanyEvaluation)
            .filter(models.CompanyEvaluation.company_id == company_id)
            .count()
        )
        return amount_of_company_evaluation_by_company_id

    except SQLAlchemyError as error:
        raise error


def get_career_development_rating_values_by_company_id(
    db: Session, company_id: int
) -> List:
    result_query = (
        db.query(models.CompanyEvaluation.career_development_rating)
        .filter(models.CompanyEvaluation.company_id == company_id)
        .all()
    )

    list_of_career_development_rating = []

    if len(result_query) > 0:
        list_of_career_development_rating = list(
            map(Util.tranform_tuple_in_string, result_query)
        )

    return list_of_career_development_rating


def get_diversity_equal_opportunity_rating_values_by_company_id(
    db: Session, company_id: int
) -> List:
    result_query = (
        db.query(models.CompanyEvaluation.diversity_equal_opportunity_rating)
        .filter(models.CompanyEvaluation.company_id == company_id)
        .all()
    )

    list_of_diversity_equal_opportunity_rating = []

    if len(result_query) > 0:
        list_of_diversity_equal_opportunity_rating = list(
            map(Util.tranform_tuple_in_string, result_query)
        )

    return list_of_diversity_equal_opportunity_rating


def get_working_environment_rating_values_by_company_id(
    db: Session, company_id: int
) -> List:
    result_query = (
        db.query(models.CompanyEvaluation.working_environment_rating)
        .filter(models.CompanyEvaluation.company_id == company_id)
        .all()
    )

    list_of_working_environment_rating = []

    if len(result_query) > 0:
        list_of_working_environment_rating = list(
            map(Util.tranform_tuple_in_string, result_query)
        )

    return list_of_working_environment_rating


def get_salary_rating_values_by_company_id(db: Session, company_id: int) -> List:
    result_query = (
        db.query(models.CompanyEvaluation.salary_rating)
        .filter(models.CompanyEvaluation.company_id == company_id)
        .all()
    )

    list_of_salary_rating = []

    if len(result_query) > 0:
        list_of_salary_rating = list(map(Util.tranform_tuple_in_string, result_query))

    return list_of_salary_rating


def calculate_gral_career_development_rating(db: Session, company_id: int):

    amount_of_company_evaluation_by_company_id = get_amount_of_company_evaluation_by_id(
        db=db, company_id=company_id
    )
    list_of_career_development_rating = (
        get_career_development_rating_values_by_company_id(db=db, company_id=company_id)
    )
    gral_rating = 0

    if amount_of_company_evaluation_by_company_id > 0:
        list_of_weight = list(
            map(Util.assign_weight, list_of_career_development_rating)
        )
        summatory_of_weigth = functools.reduce(operator.add, list_of_weight)
        result = summatory_of_weigth / amount_of_company_evaluation_by_company_id
        gral_rating = Util.round_values(result, 1)

    return gral_rating


def calculate_gral_diversity_equal_opportunity_rating(db: Session, company_id: int):

    amount_of_company_evaluation_by_company_id = get_amount_of_company_evaluation_by_id(
        db=db, company_id=company_id
    )
    list_of_diversity_equal_opportunity_rating = (
        get_diversity_equal_opportunity_rating_values_by_company_id(
            db=db, company_id=company_id
        )
    )
    gral_rating = 0

    if amount_of_company_evaluation_by_company_id > 0:
        list_of_weight = list(
            map(Util.assign_weight, list_of_diversity_equal_opportunity_rating)
        )
        summatory_of_weight = functools.reduce(operator.add, list_of_weight)
        result = summatory_of_weight / amount_of_company_evaluation_by_company_id
        gral_rating = Util.round_values(result, 1)

    return gral_rating


def calculate_gral_working_environment_rating(db: Session, company_id: int):

    amount_of_company_evaluation_by_company_id = get_amount_of_company_evaluation_by_id(
        db=db, company_id=company_id
    )
    list_of_working_environment_rating = (
        get_working_environment_rating_values_by_company_id(
            db=db, company_id=company_id
        )
    )
    gral_rating = 0

    if amount_of_company_evaluation_by_company_id > 0:
        list_of_weight = list(
            map(Util.assign_weight, list_of_working_environment_rating)
        )
        summatory_of_weight = functools.reduce(operator.add, list_of_weight)
        result = summatory_of_weight / amount_of_company_evaluation_by_company_id
        gral_rating = Util.round_values(result, 1)

    return gral_rating


def calculate_gral_salary_rating(db: Session, company_id: int):

    amount_of_company_evaluation_by_company_id = get_amount_of_company_evaluation_by_id(
        db=db, company_id=company_id
    )
    list_of_salary_rating = get_salary_rating_values_by_company_id(
        db=db, company_id=company_id
    )
    gral_rating = 0

    if amount_of_company_evaluation_by_company_id > 0:
        list_of_weight = list(map(Util.assign_weight, list_of_salary_rating))
        summatory_of_weight = functools.reduce(operator.add, list_of_weight)
        result = summatory_of_weight / amount_of_company_evaluation_by_company_id
        gral_rating = Util.round_values(result, 1)

    return gral_rating


def calculate_gral_company_rating(db: Session, company_id: int):
    gral_career_development_rating = calculate_gral_career_development_rating(
        db=db, company_id=company_id
    )
    gral_diversity_equal_opportunity_rating = (
        calculate_gral_diversity_equal_opportunity_rating(db=db, company_id=company_id)
    )
    gral_working_environment_rating = calculate_gral_working_environment_rating(
        db=db, company_id=company_id
    )
    gral_salary_rating = calculate_gral_salary_rating(db=db, company_id=company_id)

    sum_of_gral_ratings = (
        gral_career_development_rating
        + gral_diversity_equal_opportunity_rating
        + gral_working_environment_rating
        + gral_salary_rating
    )
    result = sum_of_gral_ratings / AMOUNT_OF_COMPANY_CRITERIA
    gral_company_rating = Util.round_values(result, 1)
    return gral_company_rating


def get_company_evaluations_by_company_id(
    db: Session,
    company_id: int,
    job_title: Optional[str],
    content_type: Optional[str],
    job_location: Optional[str],
    helpfulness: Optional[str],
    rating: Optional[str],
    date: Optional[str],
):
    try:
        query = db.query(models.CompanyEvaluation)

        if company_id:
            query = query.filter(models.CompanyEvaluation.company_id == company_id)

        if job_title:
            query = query.filter(
                or_(models.CompanyEvaluation.job_title.ilike(f"%{job_title}%"))
            )

        if content_type:
            query = query.filter(
                models.CompanyEvaluation.content_type.ilike(f"%{content_type}%")
            )

        if job_location:
            query = query.filter(
                or_(models.CompanyEvaluation.job_location.ilike(f"%{job_location}%"))
            )

        if rating == "DESC":
            query = query.order_by(models.CompanyEvaluation.rating.desc())

        if rating == "ASC":
            query = query.order_by(models.CompanyEvaluation.rating.asc())

        if helpfulness == "DESC":
            query = query.order_by(models.CompanyEvaluation.utility_counter.desc())

        if helpfulness == "ASC":
            query = query.order_by(models.CompanyEvaluation.utility_counter.asc())

        if date == "DESC":
            query = query.order_by(desc(models.CompanyEvaluation.created_at))

        if date == "ASC":
            query = query.order_by(asc(models.CompanyEvaluation.created_at))

        return query.order_by(models.CompanyEvaluation.id.desc()).all()

    except SQLAlchemyError as error:
        raise error


def calculate_company_evaluation_average(*args) -> float:

    average = 0

    if len(args) > 0:
        weights = list(map(Util.assign_weight, list(args)))
        total = sum(weights) / AMOUNT_OF_COMPANY_CRITERIA
        average = Util.round_values(total, 1)

    return average


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
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

            # Calculate rating average
            rating = (
                calculate_company_evaluation_average(
                    company_evaluation.career_development_rating,
                    company_evaluation.diversity_equal_opportunity_rating,
                    company_evaluation.working_environment_rating,
                    company_evaluation.salary_rating,
                ),
            )
            # Integration of the rating value
            company_evaluation.rating = rating

            db.add(company_evaluation)
            db.commit()
            db.refresh(company_evaluation)

            return company_evaluation

        except SQLAlchemyError as error:
            raise error
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")


def increse_evaluation_utility_rating(db: Session, company_evaluation_id: int) -> Dict:
    try:
        company_evaluation = get_company_evaluation_by_id(
            db=db, id=company_evaluation_id
        )
        company_evaluation.utility_counter += 1
        company_evaluation.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add(company_evaluation)
        db.commit()
        return company_evaluation
    except SQLAlchemyError as error:
        raise error


def increase_evaluation_non_utility_rating(
    db: Session, company_evaluation_id: int
) -> Dict:

    try:
        company_evaluation = get_company_evaluation_by_id(
            db=db, id=company_evaluation_id
        )
        company_evaluation.non_utility_counter += 1
        company_evaluation.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add(company_evaluation)
        db.commit()
        return company_evaluation
    except SQLAlchemyError as error:
        raise error


def get_all_reporting_reason_types(db: Session) -> List[Dict]:
    return db.query(models.ReportingReasonType).all()


def get_reporting_reason_by_id(db: Session, reporting_reason_type_id: int) -> Dict:
    return (
        db.query(models.ReportingReasonType)
        .filter(models.ReportingReasonType.id == reporting_reason_type_id)
        .first()
    )


def get_all_postulations_status(db: Session):
    try:
        return db.query(models.PostulationStatus).all()
    except SQLAlchemyError as error:
        raise error


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


def get_applicants(db: Session):
    return db.query(models.Applicant).all()


def create_applicant(
    db: Session,
    vacancy_id: int,
    name: str,
    paternal_last_name: str,
    maternal_last_name: str,
    email: EmailStr,
    cellphone: str,
    linkedin_url: HttpUrl,
    motivation_letter_url: str,
    cv_url: str,
    country: str,
    city: str,
    job_title: str,
    company: str,
):
    try:
        applicant = models.Applicant(
            vacancy_id=vacancy_id,
            postulation_status_id=1,
            name=name.capitalize().strip(),
            paternal_last_name=paternal_last_name.capitalize().strip(),
            maternal_last_name=maternal_last_name.capitalize().strip(),
            tracking_code=Util.create_tracking_code(),
            email=email.lower().strip(),
            cellphone=cellphone,
            linkedin_url=linkedin_url,
            cv_url=cv_url,
            country=country,
            city=city,
            job_title=job_title,
            company=company,
            motivation_letter_url=motivation_letter_url,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        db.add(applicant)
        db.commit()
        db.refresh(applicant)

    except SQLAlchemyError as Error:
        raise Error

    return applicant


def create_applicant_evaluation(
    db: Session,
    applicant_evaluation_body: schemas.ApplicantEvaluationCreate,
    applicant_id: int,
):

    if check_company_id_exist(company_id=applicant_evaluation_body.company_id) != -1:
        try:
            applicant_evaluation = models.ApplicantEvaluation(
                company_id=applicant_evaluation_body.company_id,
                applicant_id=applicant_id,
                applicant_name=applicant_evaluation_body.applicant_name,
                is_hired=applicant_evaluation_body.is_hired,
                communication_rating=applicant_evaluation_body.communication_rating,
                confidence_rating=applicant_evaluation_body.confidence_rating,
                negotiation_rating=applicant_evaluation_body.negotiation_rating,
                motivation_rating=applicant_evaluation_body.motivation_rating,
                self_knowledge_rating=applicant_evaluation_body.self_knowledge_rating,
                hard_skill_rating=applicant_evaluation_body.hard_skill_rating,
            )
            db.add(applicant_evaluation)
            db.commit()
            db.refresh(applicant_evaluation)

            return applicant_evaluation
        except SQLAlchemyError as error:
            raise error
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")


def create_a_recruitment_process_evaluation(
    db: Session,
    request_body: schemas.RecruitmentProcessEvaluationCreate,
    company_id: int,
):
    if get_applicant_by_id(db=db, id=request_body.applicant_id) != None:
        try:
            recruitment_process_evaluation = models.RecruitmentProcessEvaluation(
                company_id=company_id,
                applicant_id=request_body.applicant_id,
                job_title=request_body.job_title,
                improvement_content=request_body.improvement_content,
                salary_evaluation_rating=request_body.salary_evaluation_rating.value,
                allows_remote_work=request_body.allows_remote_work,
                interview_response_time_rating=request_body.interview_response_time_rating.value,
                job_description_rating=request_body.job_description_rating.value,
                is_legally_company=request_body.is_legally_company,
                amount_of_recruitment_time=request_body.amount_of_recruitment_time,
                recruitment_process_period=request_body.recruitment_process_period.value,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            db.add(recruitment_process_evaluation)
            db.commit()
            db.refresh(recruitment_process_evaluation)

            return recruitment_process_evaluation

        except SQLAlchemyError as error:
            raise error
    else:
        raise HTTPException(status_code=404, detail="Applicant Not found")


def get_application_process(db: Session, tracking_code: str, paternal_last_name: str):
    applicantion_process = (
        db.query(models.Applicant)
        .filter(
            and_(
                models.Applicant.tracking_code == tracking_code.upper().strip(),
                models.Applicant.paternal_last_name
                == paternal_last_name.capitalize().strip(),
            )
        )
        .first()
    )

    if applicantion_process != None:
        applicant = {
            "applicant_id": applicantion_process.id,
            "vacancy_id": applicantion_process.vacancy_id,
            "applicant_name": applicantion_process.name,
            "paternal_last_name": applicantion_process.paternal_last_name,
            "maternal_last_name": applicantion_process.maternal_last_name,
            "tracking_code": applicantion_process.tracking_code,
            "email": applicantion_process.email,
            "cellphone": applicantion_process.cellphone,
            "linkedin_url": applicantion_process.linkedin_url,
            "cv_url": applicantion_process.cv_url,
            "country": applicantion_process.country,
            "city": applicantion_process.city,
            "last_job_title": applicantion_process.job_title,
            "last_company_name": applicantion_process.company,
            "motivation_letter_url": applicantion_process.motivation_letter_url,
            "postulation_status_id": applicantion_process.postulation_status_id,
            "postulation_status": applicantion_process.postulation_status,
            "applicant_evaluations": applicantion_process.applicant_evaluations,
        }

        vacancy_id = applicantion_process.vacancy_id
        vacancy = get_vacancy_by_id(vacancy_id)
        result = vacancy | applicant

        return result

    else:
        raise HTTPException(
            status_code=404,
            detail="Process Application Not Found, Please check your information",
        )


def get_applicants_by_vacancy_id(db: Session, vacancy_id: int):
    try:
        applicants = (
            db.query(models.Applicant)
            .filter(models.Applicant.vacancy_id == vacancy_id)
            .all()
        )
        return applicants
    except SQLAlchemyError as error:
        raise error


def get_postulation_status_by_id(db: Session, postulations_status_id: int):
    try:
        postulations_status = (
            db.query(models.PostulationStatus)
            .filter(models.PostulationStatus.id == postulations_status_id)
            .first()
        )
        if postulations_status != None:
            return postulations_status
        else:
            raise HTTPException(status_code=404, detail="Postulation Status Not Found")
    except SQLAlchemyError as error:
        raise error


def change_postulation_status_id(
    db: Session, applicant_id: int, postulation_status_id: int
):
    try:
        applicant = get_applicant_by_id(db=db, id=applicant_id)

        applicant.postulation_status_id = postulation_status_id
        applicant.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.add(applicant)
        db.commit()
        return applicant

    except SQLAlchemyError as error:
        raise error


def get_recruitment_process_evaluations_by_company_id(db: Session, company_id: int):
    query = db.query(models.RecruitmentProcessEvaluation)
    query.filter(models.RecruitmentProcessEvaluation.company_id == company_id)
    return query.order_by(models.RecruitmentProcessEvaluation.id.desc()).all()
