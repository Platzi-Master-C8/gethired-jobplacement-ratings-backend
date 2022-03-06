# Python
from typing import List, Optional
import os
import time


# FastAPI
from fastapi import (
    FastAPI,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
    Path,
    Body,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.responses import JSONResponse
from pydantic import EmailStr, HttpUrl

# SQLAlchemy
from sqlalchemy.orm import Session

# Project
from ratings.routes import example_root
from ratings.cruds import crud
from ratings.models import models
from ratings.schemas import schemas
from ratings.config.database import SessionLocal, engine
from ratings.utils.utils import Util


models.Base.metadata.create_all(engine)


app: FastAPI = FastAPI(
    title="Jobplacement - Ratings API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_database_session():
    session_local_db = SessionLocal()
    try:
        yield session_local_db
    finally:
        session_local_db.close()


# Companies Path operations


@app.get(
    path="/api/v1/companies/{id}/general-ratings",
    tags=["Companies"],
    status_code=status.HTTP_200_OK,
    summary="Get the general ratings from a company",
)
def get_general_ratings(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, example=1, title="Company ID"),
):

    total_company_evaluations = crud.get_amount_of_company_evaluation_by_id(
        db=session_local_db, company_id=id
    )
    gral_company_rating = crud.calculate_gral_company_rating(
        db=session_local_db, company_id=id
    )
    gral_career_development_rating = crud.calculate_gral_career_development_rating(
        db=session_local_db, company_id=id
    )
    gral_diversity_equal_opportunity_rating = (
        crud.calculate_gral_diversity_equal_opportunity_rating(
            db=session_local_db, company_id=id
        )
    )
    gral_working_environment_rating = crud.calculate_gral_working_environment_rating(
        db=session_local_db, company_id=id
    )
    gral_salary_rating = crud.calculate_gral_salary_rating(
        db=session_local_db, company_id=id
    )

    company = crud.get_company_by_id(company_id=id)

    return JSONResponse(
        status_code=200,
        content={
            "data": {
                "company_information": company,
                "company_rating": gral_company_rating,
                "total_reviews": total_company_evaluations,
                "gral_career_development_rating": gral_career_development_rating,
                "gral_diversity_equal_opportunity_rating": gral_diversity_equal_opportunity_rating,
                "gral_working_environment_rating": gral_working_environment_rating,
                "gral_salary_rating": gral_salary_rating,
            },
        },
    )


# Company Evaluations Path Operations


@app.get(
    path="/api/v1/companies/{id}/company-evaluations",
    tags=["Company Evaluations"],
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.CompanyEvaluationOut],
    summary="Get Company Evaluations By Company ID",
)
def get_company_evaluations_by_company_id(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, title="Company ID", example=1, description="Company ID"),
    job_title: Optional[str] = Query(None, min_length=3, max_length=70),
    content_type: Optional[str] = Query(None, max_length=280),
    job_location: Optional[str] = Query(None, max_length=70),
    helpfulness: Optional[str] = Query(default=None, min_length=3, max_length=4),
    rating: Optional[str] = Query(default=None, min_length=3, max_length=4),
    date: Optional[str] = Query(default=None, min_length=3, max_length=4),
):
    if crud.check_company_id_exist(id) != -1:
        company_evaluations = crud.get_company_evaluations_by_company_id(
            session_local_db,
            company_id=id,
            job_title=job_title,
            content_type=content_type,
            job_location=job_location,
            helpfulness=helpfulness,
            rating=rating,
            date=date,
        )

        if len(company_evaluations) == 0:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "No evaluations have been added to this company yet",
                    "data": [],
                },
            )
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")

    return paginate(company_evaluations)


add_pagination(app)


@app.post(
    path="/api/v1/companies/{id}/company-evaluation",
    tags=["Company Evaluations"],
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CompanyEvaluationOut,
    response_description="The created company evaluation",
    summary="Create a new Company Evaluation",
)
def create_company_evaluation(
    company_evaluation: schemas.CompanyEvaluationCreate = Body(...),
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, example=1, title="Company ID", description="Company ID"),
):
    """
    This Path Operation create a company evaluation.

    # Parameters:
    - Request body parameter:
        - **job_title: str** (required) -> The name of the position you have or had in the company.
        - **content_type: str** (required) -> The content of the evaluation to be added to the company's.
        - **start_date: date** (required) -> The date on which the person started working with the company.
        - **end_date:date** (optional) -> The date on which the person finished working with the company.
        - **is_still_working_here: int** (optional) -> The date on which the person finished working with the company.
        - **applicant_email: EmailStr** (required) -> The id of the company to which this assessment belongs
        - **career_development_rating:CompanyRatingType** (required) -> It represents the rating with which the career development will be rated.
        - **diversity_equal_opportunity_rating: CompanyRatingType** (required) -> Represents the rating with which the diversity and equal opportunity will be rated.
        - **working_environment_rating: CompanyRatingType** (required) -> Represents the rating with which the work environment within the company will be rate.
        - **salary_rating: CompanyRatingType** (required) ->Represents the salary with which the work environment within the company will be rate.
        - **job_location: str** (required) -> Location of the work site.
        - **salary: decimal(12,2)** (required) -> The salary the person earned in this job.
        - **currency_type: CurrencyCodeISO4217** (required) -> The type of currency in which the company is paid.
        - **salary_frequency: SalaryFrequency** (required) -> The type of currency in which the company is paid.
        - **recommended_a_friend: int** (required) -> The type of currency in which the company is paid.
        - **allows_remote_work: int** (required) -> The company operates a remote work scheme.
        - **is_legally_company: int** (required) -> The type of currency in which the company is paid.


    # Returns:
    - The company evaluation created with this structure
        - job_title:  str
        - content_type: str
        - start_date: date
        - end_date: date
        - is_still_working_here: int
        - utility_counter: int
        - non_utility_counter: int
        - created_at: datetime
        - company_id: int
        - id: int

    """
    return crud.create_company_evaluation(
        db=session_local_db, company_evaluation=company_evaluation, company_id=id
    )


@app.patch(
    path="/api/v1/company-evaluations/{id}/increase-utility-rating",
    tags=["Company Evaluations"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.CompanyEvaluationOut,
    summary="Increases The Usefulness of a Company Assessment",
)
def increse_evaluation_utility_rating(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(
        ...,
        gt=0,
        example=1,
        title="Company Evaluation ID",
        description="Company Evaluation ID",
    ),
):
    company_evaluation = crud.get_company_evaluation_by_id(db=session_local_db, id=id)
    if company_evaluation is None:
        raise HTTPException(status_code=404, detail="Company Evaluation Not Found")

    return crud.increse_evaluation_utility_rating(
        db=session_local_db, company_evaluation_id=id
    )


@app.patch(
    path="/api/v1/company-evaluations/{id}/increase-non-utility-rating",
    tags=["Company Evaluations"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.CompanyEvaluationOut,
    summary="Increases The Non-utility of a Company Evaluation",
)
def increse_evaluation_non_utility_rating(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(
        ...,
        gt=0,
        example=1,
        title="Company Evaluation ID",
        description="Company Evaluation ID",
    ),
):

    company_evaluation = crud.get_company_evaluation_by_id(db=session_local_db, id=id)
    if company_evaluation is None:
        raise HTTPException(status_code=404, detail="Company Evaluation Not Found")

    return crud.increase_evaluation_non_utility_rating(
        db=session_local_db, company_evaluation_id=id
    )


@app.post(
    path="/api/v1/company-evaluation/{id}/complaints",
    response_model=schemas.ComplaintOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Company Evaluations"],
    summary="Create a complaint to a company evaluation",
)
def create_a_company_evaluation_report(
    session_local_db: Session = Depends(get_database_session),
    complaint_body: schemas.ComplaintCreate = Body(...),
    id: int = Path(
        ...,
        gt=0,
        title="Company Evaluation ID",
        description="Company Evaluation ID",
    ),
):
    reporting_reason_type_id = crud.get_reporting_reason_by_id(
        db=session_local_db,
        reporting_reason_type_id=complaint_body.reporting_reason_type_id,
    )

    if reporting_reason_type_id is None:
        raise HTTPException(
            status_code=404, detail="Reporting Reason Type ID Not Found"
        )

    company_evaluation_id = crud.get_company_evaluation_by_id(
        db=session_local_db, id=id
    )

    if company_evaluation_id is None:

        raise HTTPException(status_code=404, detail="Company Evaluation Not Found")

    return crud.create_complaint(
        db=session_local_db, complaint_body=complaint_body, company_evaluation_id=id
    )


# Reporting Reason type Path operation


@app.get(
    path="/api/v1/reporting-reason-types",
    response_model=List[schemas.ReportingReasonTypeOut],
    status_code=status.HTTP_200_OK,
    tags=["Reporting Reason Types"],
    summary="Get the List of Reporting Reason Types",
)
def get_reporting_reason_types(
    session_local_db: Session = Depends(get_database_session),
):
    return crud.get_all_reporting_reason_types(db=session_local_db)


# Applicants path operations


@app.post(
    path="/api/v1/applicants",
    response_model=schemas.ApplicantOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Applicants"],
    summary="Register an Applicant who applies to a vacancy.",
)
def register_applicants(
    vacancy_id: int = Form(..., gt=0, title="Vacancy ID", description="Vacancy ID"),
    name: str = Form(
        ..., max_length=40, title="Applicant Name", description="Applicant Name"
    ),
    paternal_last_name: str = Form(
        ..., max_length=40, title="paternal_last_name", description="Paternal Last Name"
    ),
    maternal_last_name: str = Form(
        ..., max_length=40, title="maternal_last_name", description="Maternal Last Name"
    ),
    email: EmailStr = Form(..., title="email", description="Applicant's Email"),
    cellphone: str = Form(
        ...,
        max_length=13,
        title="cellphone",
        description="Applicant's cellphone",
    ),
    linkedin_url: HttpUrl = Form(
        default=None,
        title="linkedin_url",
        description="Applicant's linkedin url",
    ),
    cv_file: UploadFile = File(..., title="CV File", description="CV File"),
    motivation_letter_file: UploadFile = File(
        default=None, title="Motivation Letter", description="Motivation Letter File"
    ),
    country: str = Form(..., title="Country", max_length=70, description="Country"),
    city: str = Form(..., title="Country", max_length=70, description="Country"),
    job_title: str = Form(
        default=None, title="Job Title", max_length=70, description="Job title"
    ),
    company: str = Form(
        default=None,
        title="Company",
        max_length=150,
        description="Last company in which the applicant worked",
    ),
    session_local_db: Session = Depends(get_database_session),
):
    if crud.check_vacancy_id_exist(vacancy_id=vacancy_id) != -1:

        ROOT_DIR = os.getcwd()
        # Save the cv files
        if not cv_file:
            cv_file_name = None

        elif cv_file.content_type not in ["application/pdf"]:
            raise HTTPException(400, detail="Invalid document type")
        else:
            cv_file_name = f"cv_{int(time.time())}.pdf"
            file_location_cv = f"/static/{cv_file_name}"
            with open(ROOT_DIR + file_location_cv, "wb+") as file_object:
                file_object.write(cv_file.file.read())

        # Save the motivation letter
        if not motivation_letter_file:
            motivation_letter_file_name = None

        elif motivation_letter_file.content_type not in ["application/pdf"]:
            raise HTTPException(400, detail="Invalid document type")

        else:
            motivation_letter_file_name = f"ml_{int(time.time())}.pdf"
            file_location_motivation_letter = (
                f"/static/{motivation_letter_file_name}.pdf"
            )
            with open(ROOT_DIR + file_location_motivation_letter, "wb+") as file_object:
                file_object.write(motivation_letter_file.file.read())

        applicant = crud.create_applicant(
            db=session_local_db,
            vacancy_id=vacancy_id,
            name=name,
            paternal_last_name=paternal_last_name,
            maternal_last_name=maternal_last_name,
            email=email,
            cellphone=cellphone,
            linkedin_url=linkedin_url,
            cv_url=cv_file_name,
            motivation_letter_url=motivation_letter_file_name,
            country=country,
            city=city,
            job_title=job_title,
            company=company,
        )

        # Send Email
        Util.send_offer_tracking_email(
            applicant.email, applicant.tracking_code, applicant.paternal_last_name
        )

        # integration of applicant in enterprise database
        crud.create_vacancy_applicant(vacancy_id=vacancy_id, applicant_id=applicant.id)

        return applicant
    else:
        raise HTTPException(status_code=404, detail="Vacancy Not Found")


@app.post(
    path="/api/v1/applicants/{id}/applicant-evaluation",
    tags=["Applicants"],
    response_model=schemas.ApplicantEvaluationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create an Applicant Evaluation",
)
def create_applicant_evaluation(
    session_local_db: Session = Depends(get_database_session),
    applicant_evaluation_body: schemas.ApplicantEvaluationCreate = Body(...),
    id: int = Path(
        ...,
        ge=0,
        title="Applicant ID",
        description="Applicant ID",
    ),
):
    if crud.get_applicant_by_id(db=session_local_db, id=id) is None:
        raise HTTPException(status_code=404, detail="Applicant Not Found")

    return crud.create_applicant_evaluation(
        db=session_local_db,
        applicant_evaluation_body=applicant_evaluation_body,
        applicant_id=id,
    )


@app.post(
    path="/api/v1/companies/{id}/recruitment-process-evaluation",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.RecruitmentProcessEvaluationOut,
    tags=["Applicants"],
    summary="Create a Recruitment Process Evaluation to a company",
)
def create_recruitment_process_evaluation(
    session_local_db: Session = Depends(get_database_session),
    request_body: schemas.RecruitmentProcessEvaluationCreate = Body(...),
    id: int = Path(..., gt=0, title="Company ID", description="Company ID"),
):
    if crud.check_company_id_exist(company_id=id) == -1:
        raise HTTPException(status_code=404, detail="Company Not found")

    return crud.create_a_recruitment_process_evaluation(
        db=session_local_db, request_body=request_body, company_id=id
    )


@app.get(
    path="/api/v1/applicants/{tracking_code}/{paternal_last_name}/applicant-review",
    tags=["Applicants"],
    status_code=status.HTTP_200_OK,
)
def get_application_process(
    session_local_db: Session = Depends(get_database_session),
    tracking_code: str = Path(
        ..., max_length=8, title="Tracking Code", description="Tracking Code"
    ),
    paternal_last_name: str = Path(
        ..., max_length=70, title="Paternal Last Name", description="Paternal Last Name"
    ),
):

    applicant_process = crud.get_application_process(
        db=session_local_db,
        tracking_code=tracking_code,
        paternal_last_name=paternal_last_name,
    )
    if applicant_process is None:
        raise HTTPException(
            status_code=404,
            detail="Process Application Not Found, Please check your information",
        )

    return applicant_process


@app.get(
    path="/api/v1/postulation-status",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.PostulationStatusOut],
    tags=["Postulation status"],
    summary="Get a List of Postulation Status",
)
def get_postulation_status_list(
    session_local_db: Session = Depends(get_database_session),
):

    postulation_list = crud.get_all_postulations_status(db=session_local_db)
    if len(postulation_list) == 0:
        return JSONResponse(
            status_code=200,
            content={
                "message": "No evaluations have been added to this company yet",
                "data": [],
            },
        )
    return postulation_list


@app.get(
    path="/api/v1/vacancies/{vacancy_id}/applicants",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ApplicantOut],
    tags=["Vacancies"],
    summary="Get a List of Applicant Who Has Apply to a Specific Vacancy",
)
def get_applicants_by_vacancy_id(
    session_local_db: Session = Depends(get_database_session),
    vacancy_id: int = Path(..., gt=0, title="Vacancy ID", description="Vacancy ID"),
):
    if crud.check_vacancy_id_exist(vacancy_id=vacancy_id) != -1:
        applicants = crud.get_applicants_by_vacancy_id(
            db=session_local_db, vacancy_id=vacancy_id
        )

        if len(applicants) == 0:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "No Applicants have been added to the vacancy",
                    "data": [],
                },
            )
        return applicants
    else:
        raise HTTPException(status_code=404, detail="Vacancy Not Found")


@app.get(
    path="/api/v1/applicants/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ApplicantOut],
    tags=["Applicants"],
    summary="List all Applicants",
)
def get_all_applicants(session_local_db: Session = Depends(get_database_session)):
    return crud.get_applicants(db=session_local_db)


@app.get(
    path="/api/v1/applicants/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ApplicantOut,
    tags=["Applicants"],
    summary="Get an Applicant by ID",
)
def get_applicant_by_id(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, title="Applicant ID", description="Applicant ID"),
):
    return crud.get_applicant_by_id(db=session_local_db, id=id)


@app.patch(
    path="/api/v1/applicants/{id}/postulation-status/{postulation_status_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ApplicantOut,
    tags=["Applicants"],
    summary="Change an Applicant's Application Status",
)
def get_applicant_by_id(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, title="Applicant ID", description="Applicant ID"),
    postulation_status_id: int = Path(
        ..., gt=0, title="Postulation Status ID", description="Postulation Status ID"
    ),
):

    if crud.get_applicant_by_id(db=session_local_db, id=id) is None:
        raise HTTPException(status_code=404, detail="Applicant Not Found")

    if (
        crud.get_postulation_status_by_id(
            db=session_local_db, postulations_status_id=postulation_status_id
        )
        is None
    ):
        raise HTTPException(status_code=404, detail="Postulation Status Mot Found")

    return crud.change_postulation_status_id(
        db=session_local_db,
        applicant_id=id,
        postulation_status_id=postulation_status_id,
    )


@app.get(
    path="/api/v1/companies/{id}/recruitment-process-evaluations",
    status_code=status.HTTP_200_OK,
    response_model=Page[schemas.RecruitmentProcessEvaluationOut],
    tags=["Companies"],
    summary="Get a list of recruitment process evaluation per company",
)
def get_all_recruitment_process_evaluations(
    session_local_db: Session = Depends(get_database_session),
    id: int = Path(..., gt=0, title="Company ID", example=1, description="Company ID"),
):
    if crud.check_company_id_exist(id) != -1:
        recruitment_process_evaluations = (
            crud.get_recruitment_process_evaluations_by_company_id(
                db=session_local_db, company_id=id
            )
        )
        return paginate(recruitment_process_evaluations)
    else:
        raise HTTPException(status_code=404, detail="Company Not Found")
