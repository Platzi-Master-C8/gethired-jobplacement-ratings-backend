# Python

# SQLAlchemy
from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Project
from ratings.config.database import Base


class CompanyEvaluation(Base):
    """Company Evaluation."""

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
    """Reporting Reason Type."""

    __tablename__ = "reporting_reason_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    items = relationship("Complaint", back_populates="type_report")


class Complaint(Base):
    """Complaints."""

    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    problem_description = Column(String(70), nullable=False)
    email = Column(String(70), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    reporting_reason_type_id = Column(Integer, ForeignKey("reporting_reason_types.id"))

    # Relationships
    type_report = relationship("ReportingReasonType", back_populates="items")


class CompanyEvaluationComplaint(Base):
    """Table pivot between Company Evaluation and Complaints."""

    __tablename__ = "company_evaluation_complaint"

    id = Column(Integer, primary_key=True, index=True)
    company_evaluation_id = Column(Integer, ForeignKey("company_evaluations.id"))
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
