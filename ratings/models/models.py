from sqlalchemy import Column, Integer, String, DECIMAL, false, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ratings.config.database import Base


class CompanyEvaluation(Base):
    __tablename__ = "company_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, index=True)
    job_title = Column(String(70), nullable=false)
    content_type = Column(String(250), nullable=false)
    career_development_rating = Column(String(15), nullable=false)
    diversity_equal_opportunity_rating = Column(String(15), nullable=false)
    working_environment_rating = Column(String(15), nullable=false)
    salary_rating = Column(String(15), nullable=false)
    job_location = Column(String(70), nullable=false)
    applicant_email = Column(String(70), nullable=false)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_still_working_here = Column(Integer)
    salary = Column(DECIMAL(14, 2), nullable=false)
    currency_type = Column(String(5), nullable=false)
    salary_frequency = Column(String(15), nullable=false)
    recommended_a_friend = Column(Integer, nullable=false)
    allows_remote_work = Column(Integer, nullable=false)
    is_legally_company = Column(Integer, nullable=false)
    utility_counter = Column(Integer, default=0)
    non_utility_counter = Column(Integer, default=0)
    created_at = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=text('now()')
    )

    complaints = relationship(
        "Complaint",
        secondary="company_evaluation_complaint",
    )


class ReportingReasonType(Base):
    __tablename__ = "reporting_reason_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=text('now()')
    )

    items = relationship("Complaint", back_populates="type_report")


class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    problem_description = Column(
        String(70),
        nullable=False
    )
    email = Column(
        String(70),
        nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=text('now()')
    )
    reporting_reason_type_id = Column(
        Integer,
        ForeignKey("reporting_reason_types.id")
    )

    type_report = relationship("ReportingReasonType", back_populates="items")


class CompanyEvaluationComplaint(Base):
    __tablename__ = "company_evaluation_complaint"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    company_evaluation_id = Column(
        Integer,
        ForeignKey("company_evaluations.id")
    )
    complaint_id = Column(
        Integer,
        ForeignKey("complaints.id")
    )
    created_at = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=text('now()')
    )
