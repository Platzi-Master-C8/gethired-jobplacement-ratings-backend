from datetime import datetime

from typing import Optional

from pydantic import BaseModel


class CompanyEvaluationBase(BaseModel):
    job_title: str
    content_type: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_still_working_here: int


class CompanyEvaluationCreate(CompanyEvaluationBase):
    applicant_email: str
    career_development_rating: str
    diversity_equal_opportunity_rating: str
    working_environment_rating: str
    salary_rating: str
    job_location: str
    salary: float
    recommended_a_friend:  int
    allows_remote_work:  int
    is_legally_company: int


class CompanyEvaluation(CompanyEvaluationBase):
    id: int
    company_id: int
    created_at: Optional[datetime] = None

    class config:
        orm_mode = True
