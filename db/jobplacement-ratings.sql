CREATE DATABASE "jobplacement-ratings"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

\c jobplacement-ratings;

CREATE TABLE company_evaluations
(
    id bigserial NOT NULL,
    company_id bigint NOT NULL,
    job_title VARCHAR(70) NOT NULL,
    content_type VARCHAR(280) NOT NULL,
    career_development_rating VARCHAR(15) NOT NULL,
    diversity_equal_opportunity_rating VARCHAR(15) NOT NULL,
    working_environment_rating VARCHAR(15) NOT NULL,
    salary_rating VARCHAR(15) NOT NULL,
    job_location VARCHAR(70) NOT NULL,
    applicant_email VARCHAR(70) NOT NULL,
    start_date date NOT NULL,
    end_date date,
    is_still_working_here smallint,
    salary DECIMAL(12, 2) NOT NULL,
    currency_type VARCHAR(5) NOT NULL,
    salary_frequency VARCHAR(15) NOT NULL,
    recommended_a_friend smallint NOT NULL,
    allows_remote_work smallint NOT NULL,
    is_legally_company smallint NOT NULL,
    utility_counter BIGINT,
    non_utility_counter BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT career_development_rating_check CHECK (career_development_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT diversity_equal_opportunity_rating_check CHECK (diversity_equal_opportunity_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT working_environment_rating_check CHECK (working_environment_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT currency_type_check CHECK (currency_type = ANY (ARRAY['MXN', 'COP', 'CLP', 'USD', 'EUR'])),
    CONSTRAINT salary_rating_check CHECK (salary_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT salary_frequency_check CHECK (salary_frequency= ANY (ARRAY['Hour', 'Day', 'Month', 'Year'])),
    CONSTRAINT is_still_working_here_check CHECK (is_still_working_here = ANY (ARRAY[1, 0])),
    CONSTRAINT recommended_a_friend_check CHECK (recommended_a_friend = ANY (ARRAY[1, 0])),
    CONSTRAINT allows_remote_work_check CHECK (allows_remote_work = ANY (ARRAY[1, 0])),
    CONSTRAINT is_legally_company_check CHECK (is_legally_company = ANY (ARRAY[1, 0]))
);

ALTER TABLE IF EXISTS company_evaluations
    OWNER to postgres;

CREATE TABLE applicants (
    id bigserial NOT NULL,
    name VARCHAR(70) NOT NULL,
    email VARCHAR(70) NOT NULL,
    address VARCHAR(150),
    telephone VARCHAR(10) NOT NULL,
    linkedln_url VARCHAR(150),
    cv_url VARCHAR(150) NOT NULL,
    motivation_letter_url VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT email_unique UNIQUE (email)
);

CREATE TABLE reporting_reason_types(
    id bigserial NOT NULL,
    name VARCHAR(70) not NULL,
    description VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE complaints(
    id bigserial NOT NULL,
    reporting_reason_type_id BIGINT NOT NULL,
    problem_description VARCHAR(70) NOT NULL,
    email VARCHAR(70) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY (reporting_reason_type_id) REFERENCES reporting_reason_types(id)
);


CREATE TABLE company_applicant_evaluation(
    id bigserial NOT NULL,
    company_id BIGINT NOT NULL,
    applicant_id BIGINT NOT NULL,
    applicant_name VARCHAR (50) NOT NULL,
    is_hired SMALLINT NOT NULL,
    communication_rating SMALLINT NOT NULL,
    confidence_rating SMALLINT NOT NULL,
    negotiation_rating SMALLINT NOT NULL,
    motivation_rating SMALLINT NOT NULL,
    self_knowledge_rating SMALLINT NOT NULL,
    hard_skill_rating SMALLINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY(applicant_id) REFERENCES applicants(id),
    CONSTRAINT is_hired_check CHECK (is_hired = ANY (ARRAY[1,0])),
    CONSTRAINT communication_rating_check CHECK (communication_rating = ANY (ARRAY[1, 2, 3, 4, 5])),
    CONSTRAINT confidence_rating_check CHECK (confidence_rating = ANY (ARRAY[1, 2, 3, 4, 5])),
    CONSTRAINT negotiation_rating_check CHECK (negotiation_rating = ANY (ARRAY[1, 2, 3, 4, 5])),
    CONSTRAINT motivation_rating_check CHECK (motivation_rating = ANY (ARRAY[1, 2, 3, 4, 5])),
    CONSTRAINT self_knowledge_rating_check CHECK (self_knowledge_rating = ANY (ARRAY[1, 2, 3, 4, 5])),
    CONSTRAINT hard_skill_rating_check CHECK (hard_skill_rating = ANY (ARRAY[1, 2, 3, 4, 5]))

);

CREATE TABLE company_evaluation_complaint (
    id bigserial NOT NULL,
    company_evaluation_id BIGINT NOT NULL,
    complaint_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (company_evaluation_id) REFERENCES company_evaluations(id),
    FOREIGN KEY (complaint_id) REFERENCES complaints(id)
);


CREATE TABLE recruitment_process_evaluations(
    id bigserial NOT NULL,
    company_id BIGINT NOT NULL,
    applicant_id BIGINT NOT NULL,
    job_title VARCHAR(70) NOT NULL,
    improvement_content VARCHAR(250) NOT NULL,
    salary_evaluation_rating VARCHAR(15) NOT NULL,
    allows_remote_work SMALLINT NOT NULL,
    interview_response_time_rating VARCHAR(15) NOT NULL,
    job_description_rating VARCHAR(15) NOT NULL,
    is_legally_company SMALLINT NOT NULL,
    amount_of_recruitment_time INTEGER NOT NULL,
    recruitment_process_period VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    CONSTRAINT allows_remote_work_check CHECK (allows_remote_work = ANY (ARRAY[1,0])),
    CONSTRAINT is_legally_company_check CHECK (is_legally_company = ANY (ARRAY[1,2])),
    CONSTRAINT salary_evaluation_rating_check CHECK (salary_evaluation_rating = ANY (ARRAY['High','Average','Low'])),
    CONSTRAINT interview_response_time_rating_check CHECK (interview_response_time_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT job_description_rating_check CHECK (job_description_rating = ANY (ARRAY['Good', 'Regular', 'Bad'])),
    CONSTRAINT recruitment_process_period_check CHECK (recruitment_process_period = ANY (ARRAY['Hour', 'Day', 'Month','Year']))
);



INSERT INTO reporting_reason_types(name) VALUES ('Suspicious, spam or fake');
INSERT INTO reporting_reason_types(name) VALUES ('Harassment or incitement to hatred');
INSERT INTO reporting_reason_types(name) VALUES ('Violence or physical assault');
INSERT INTO reporting_reason_types(name) VALUES ('Violence or physical assault');
INSERT INTO reporting_reason_types(name) VALUES ('Adult content');
INSERT INTO reporting_reason_types(name) VALUES ('Defamation or infringement of intellectual property');
INSERT INTO reporting_reason_types(name) VALUES ('None of the reasons for reporting apply');