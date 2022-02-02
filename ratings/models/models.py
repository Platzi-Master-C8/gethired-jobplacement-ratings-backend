# Python

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Project
from ratings.config.database import Base


class CompanyEvaluation(Base):

    __tablename__ = "company_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    job_title = Column(String(70), nullable=False)
    content_type = Column(String(250), nullable=False)
    career_development_rating = Column(String(15), nullable=False)
    diversity_equal_opportunity_rating = Column(String(15), nullable=False)
    working_environment_rating = Column(String(15), nullable=False)
    salary_rating = Column(String(15), nullable=False)
    job_location = Column(String(70), nullable=False)
    applicant_email = Column(String(70), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_still_working_here = Column(Integer)
    salary = Column(DECIMAL(12, 2), nullable=False)
    currency_type = Column(String(5), nullable=False)
    salary_frequency = Column(String(15), nullable=False)
    recommended_a_friend = Column(Integer, nullable=False)
    allows_remote_work = Column(Integer, nullable=False)
    is_legally_company = Column(Integer, nullable=False)
    utility_counter = Column(Integer, default=0)
    non_utility_counter = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    complaints = relationship(
        "Complaint",
        secondary="company_evaluation_complaint",
    )


class ReportingReasonType(Base):

    __tablename__ = "reporting_reason_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    items = relationship("Complaint", back_populates="type_report")


class Complaint(Base):

    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    problem_description = Column(String(70), nullable=False)
    email = Column(String(70), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    reporting_reason_type_id = Column(Integer, ForeignKey("reporting_reason_types.id"))

    # Relationships
    type_report = relationship("ReportingReasonType", back_populates="items")


class CompanyEvaluationComplaint(Base):

    __tablename__ = "company_evaluation_complaint"

    id = Column(Integer, primary_key=True, index=True)
    company_evaluation_id = Column(Integer, ForeignKey("company_evaluations.id"))
    complaint_id = Column(Integer, ForeignKey("complaints.id"))


class Applicant(Base):

    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), nullable=False)
    paternal_last_name = Column(String(40), nullable=False)
    maternal_last_name = Column(String(40), nullable=False)
    tracking_code = Column(String(8), nullable=False)
    email = Column(String(70), nullable=False)
    address = Column(String(150), nullable=False)
    cellphone = Column(String(10), nullable=True)
    linkedln_url = Column(String(2083), nullable=True)
    cv_url = Column(String(150), nullable=False)
    motivation_letter_url = Column(String(150), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    applicant_evaluations = relationship(
        "ApplicantEvaluation", back_populates="applicant"
    )


class ApplicantEvaluation(Base):

    __tablename__ = "applicant_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False)
    applicant_name = Column(String(50), nullable=False)
    is_hired = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    confidence_rating = Column(Integer, nullable=False)
    negotiation_rating = Column(Integer, nullable=False)
    motivation_rating = Column(Integer, nullable=False)
    self_knowledge_rating = Column(Integer, nullable=False)
    hard_skill_rating = Column(Integer, nullable=False)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    created_at = Column(DateTime, server_default=func.now())

    applicant = relationship("Applicant", back_populates="applicant_evaluations")
