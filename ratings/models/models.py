from sqlalchemy import Column, Integer, String, DECIMAL, false, Date
from sqlalchemy.sql.sqltypes import TIMESTAMP
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
    # created_at = Column(DateTime(), default=datetime.now())


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(70), nullable=False)
    address = Column(String(70), nullable=True)
    telephone = Column(Integer(10), nullable=True)
    linkedln_url = Column(String(150), nullable=False)
    cv_url = Column(String(150), nullable=False)
    motivation_letter_url = Column(String(150), nullable=True)
