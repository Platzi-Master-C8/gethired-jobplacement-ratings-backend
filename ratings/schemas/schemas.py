from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from ratings.routes import example
from ratings.utils import enums


class CompanyEvaluationBase(BaseModel):
    company_id: int = Field(
        ...,
        gt=0,
        example=1,
        title="This is the id of the provenient company",
        extra="This field is validate to be grather than 0"
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
        example="Excellent company, they are very united and loyal to their values and their culture of never stop learning."
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
        example="maribel@gmail.com"
    )
    career_development_rating: enums.CompanyRatingType = Field(
        ...,
        example="Good"
    )
    diversity_equal_opportunity_rating: enums.CompanyRatingType = Field(
        ...,
        example="Good"
    )
    working_environment_rating: enums.CompanyRatingType = Field(
        ...,
        example="Good"
    )
    salary_rating: enums.CompanyRatingType = Field(
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
    currency_type: enums.CurrencyCodeISO4217 = Field(
        ...,
        example="USD"
    )
    salary_frequency: enums.SalaryFrecuency = Field(
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


class CompanyEvaluationOut(CompanyEvaluationBase):
    utility_counter: Optional[int] = Field(
        None,
        example=15,
        title="Represents the number of times the evaluation was rated as useful.",
    )
    non_utility_counter: Optional[int] = Field(
        None,
        example=2,
        title="Represents the number of times the evaluation was rated as not useful.",
    )
    created_at: Optional[datetime] = Field(
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    id: int = Field(
        gt=0,
        example=1
    )

    class Config:
        orm_mode = True


class ReportingReasonTypeBase(BaseModel):
    name: str = Field(
        ...,
        min_length=10,
        max_length=70,
        title="Name of the reason type of report",
        example="Suspicious, spam or fake"
    )


class ReportingReasonTypeCreate(ReportingReasonTypeBase):
    description: Optional[str] = Field(
        min_length=10,
        max_length=150,
        title="Description of the reporting reason type"
    )


class ReportingReasonTypeOut(ReportingReasonTypeBase):
    id: int = Field(
        ...,
        gt=0,
        title="This is the identifier of a Reportig Reason Type",
        example=1
    )

    class Config:
        orm_mode = True


class ComplaintBase(BaseModel):
    reporting_reason_type_id: int = Field(
        ...,
        gt=0,
        title="This is the id of one valid Reporting Reason Type",
        example=1
    )
    problem_description: str = Field(
        ...,
        min_length=10,
        max_length=70,
        description="Description of the problem with the company evaluation",
        example="It is a fake evaluation"
    )
    email: str = Field(
        ...,
        min_length=11,
        max_length=70,
        example="email@gmail.com"
    )


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintOut(ComplaintBase):
    id: int = Field(
        ...,
        gt=0,
        title="Complaint Id",
        example=1
    )

    class Config:
        orm_mode = True
