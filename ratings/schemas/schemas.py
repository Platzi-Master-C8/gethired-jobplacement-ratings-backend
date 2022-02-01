# Python
from datetime import date, datetime
from typing import List, Optional

# Pydantic
from pydantic import BaseModel, EmailStr, Field, HttpUrl, condecimal

# Project
from ratings.routes import example
from ratings.utils import enums


class CompanyEvaluationBase(BaseModel):
    job_title: str = Field(..., min_length=3, max_length=70, example="Backend Engineer")
    content_type: str = Field(
        ...,
        max_length=280,
        example="Excellent company, they are very united and loyal to their values and their culture.",
    )
    start_date: date = Field(..., example="2021-01-01")
    end_date: Optional[date] = Field(default=None, example="2022-01-01")
    is_still_working_here: int = Field(default=None, le=1, ge=0, example=0)


class CompanyEvaluationCreate(CompanyEvaluationBase):
    applicant_email: EmailStr = Field(..., example="maribel@gmail.com")
    career_development_rating: enums.CompanyRatingType = Field(..., example="Good")
    diversity_equal_opportunity_rating: enums.CompanyRatingType = Field(
        ..., example="Good"
    )
    working_environment_rating: enums.CompanyRatingType = Field(..., example="Good")
    salary_rating: enums.CompanyRatingType = Field(..., example="Good")
    job_location: str = Field(..., example="Mexico")
    salary: condecimal(gt=0, max_digits=12, decimal_places=2) = Field(
        ...,
        example=2500.00,
    )
    currency_type: enums.CurrencyCodeISO4217 = Field(..., example="USD")
    salary_frequency: enums.SalaryFrequency = Field(..., example="Month")
    recommended_a_friend: int = Field(..., le=1, ge=0, example=1)
    allows_remote_work: int = Field(..., le=1, ge=0, example=1)
    is_legally_company: int = Field(..., le=1, ge=0, example=1)


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
        None, example=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    company_id: int = Field(
        ...,
        gt=0,
        example=1,
        title="Company id",
        extra="This field is validate to be grater than 0",
    )
    id: int = Field(gt=0, example=1)

    class Config:
        orm_mode = True


class ReportingReasonTypeBase(BaseModel):
    name: str = Field(
        ...,
        min_length=10,
        max_length=70,
        title="Name of the reason type of report",
        example="Suspicious, spam or fake",
    )


class ReportingReasonTypeCreate(ReportingReasonTypeBase):
    description: Optional[str] = Field(
        min_length=10, max_length=150, title="Description of the reporting reason type"
    )


class ReportingReasonTypeOut(ReportingReasonTypeBase):
    id: int = Field(
        ..., gt=0, title="This is the identifier of a Reporting Reason Type", example=1
    )

    class Config:
        orm_mode = True


class ComplaintBase(BaseModel):
    reporting_reason_type_id: int = Field(
        ..., gt=0, title="This is the id of one valid Reporting Reason Type", example=1
    )
    problem_description: str = Field(
        ...,
        min_length=10,
        max_length=70,
        description="Description of the problem with the company evaluation",
        example="It is a fake evaluation",
    )
    email: str = Field(..., min_length=11, max_length=70, example="jose@gmail.com")


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintOut(ComplaintBase):
    id: int = Field(..., gt=0, title="Complaint ID", example=1)

    class Config:
        orm_mode = True


class ApplicantBase(BaseModel):
    name: str = Field(
        ..., max_length=40, description="Applicant Name", example="Javier"
    )
    paternal_last_name: str = Field(
        ..., max_length=40, description="Applicant Name", example="Amaya"
    )
    maternal_last_name: str = Field(
        ..., max_length=40, description="Applicant Name", example="Patricio"
    )
    email: EmailStr = Field(..., example="javieramayapat@gmail.com")
    address: str = Field(
        max_length=150,
        title="Address",
        example="CARRERA 7 71 21 PISO 18 TORRE A, BOGOTA, BOGOTA",
    )
    cellphone: int = Field(..., title="Cellphone", example="7441487566")
    linkedln_url: HttpUrl = Field(
        default=None,
        title="Linkedln URL",
        example="https://www.linkedin.com/in/javieramayapat/",
    )


class ApplicantCreate(ApplicantBase):
    pass


class ApplicantOut(ApplicantBase):
    cv_url: str = Field(...)
    motivation_letter_url: str = Field(default=None)
    tracking_code: str = Field(
        ..., max_length=8, title="Tracking Code", example="ADER543J"
    )
    id: int = Field(..., gt=0, title="Applicant ID", example=1)

    class Config:
        orm_mode = True
