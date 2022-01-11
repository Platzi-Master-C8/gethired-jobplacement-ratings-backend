from datetime import date
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class CompanyEvaluationBase(BaseModel):
    company_id: int = Field(
        ...,
        gt=0,
        example=1
    )
    job_title: str = Field(
        ...,
        min_length=3,
        max_length=70,
        example="Backend Engineer"
    )
    content_type: str = Field(
        ...,
        max_length=280,
        example= "Muy buena Empresa Para Trabajar remoto"
    )
    start_date: date = Field(
        ...,
        example="2021-01-01"
    )
    end_date: Optional[date] = Field(
        default=None,
        example="2022-01-01"
    )
    is_still_working_here: int = Field(
        default=None,
        le=1,
        ge=0,
        example=0
    )


class CompanyEvaluationCreate(CompanyEvaluationBase):
    applicant_email: str = Field(
        ...,
        example="anabelisa@gmail.com"
    )
    career_development_rating: str = Field(
        ...,
        example="Good"
    )
    diversity_equal_opportunity_rating: str = Field(
        ...,
        example="Good"
    )
    working_environment_rating: str = Field(
        ...,
        example="Good"
    )
    salary_rating: str = Field(
        ...,
        example="Good"
    )
    job_location: str = Field(
        ...,
        example="México"
    )
    salary: int = Field(
        ...,
        example=2500
    )
    currency_type: str = Field(
        ...,
        example="USD"
    )
    salary_frequency: str = Field(
        ...,
        example="Month"
    )
    recommended_a_friend:  int = Field(
        ...,
        le=1,
        ge=0,
        example=1
    )
    allows_remote_work: int = Field(
        ...,
        le=1,
        ge=0,
        example=1
    )
    is_legally_company: int = Field(
        ...,
        le=1,
        ge=0,
        example=1
    )


class CompanyEvaluation(CompanyEvaluationBase):
    id: int = Field(
        gt=0
    )

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

    class Config:
        orm_mode = True
