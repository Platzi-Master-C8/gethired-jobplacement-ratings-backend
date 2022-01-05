from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class CompanyEvaluationBase(BaseModel):
    company_id: int
    job_title: str
    content_type: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_still_working_here: int


class CompanyEvaluationCreate(CompanyEvaluationBase):
    applicant_email: str
    career_development_rating: str
    diversity_equal_opportunity_rating: str
    working_environment_rating: str
    salary_rating: str
    job_location: str
    salary: float
    currency_type: str
    salary_frequency: str
    recommended_a_friend:  int
    allows_remote_work:  int
    is_legally_company: int


class CompanyEvaluation(CompanyEvaluationBase):
    id: int

    class Config:
        orm_mode = True


class ApplicantBase(BaseModel):
    name: str
    email: str
    address: str
    telephone: Optional[int] = None
    linkedln_url: Optional[str] = None
    cv_url: Optional[str]
    motivation_letter_url: Optional[str] = None


class ApplicantCreate(ApplicantBase):
    pass


class Applicant(ApplicantBase):
    id: int
