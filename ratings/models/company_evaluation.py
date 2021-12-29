from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, false, Date, BigInteger, SmallInteger
from ..config.database import Base


class CompanyEvaluation(Base):
    __tablename__ = "company_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(BigInteger, index=True)
    job_title = Column(String(70), nullable=false)
    content_type = Column(String(250), nullable=false)
    career_development_rating = Column(String(15), nullable=false)
    diversity_equal_opportunity_rating = Column(String(15), nullable=false)
    working_environment_rating = Column(String(15), nullable=false)
    salary_rating = Column(String(15), nullable=false)
    job_location = Column(String(70), nullable=false)
    applicant_email = Column(String(70), nullable=false)
    start_date = Column(Date)
    end_date = Column(Date)
    is_still_working_here = Column(SmallInteger)
    salary = Column(DECIMAL(14, 2), nullable=false)
    currency_type = Column(String(5), nullable=false)
    salary_frequency = Column(String(15), nullable=false)
    recommended_a_friend = Column(SmallInteger, nullable=false)
    remote_work_allowed = Column(SmallInteger, nullable=false)
    is_legally_company = Column(SmallInteger, nullable=false)
    utility_counter = Column(BigInteger)
    non_utility_counter = Column(BigInteger)
    created_at = Column(DateTime(), default=datetime.now())
