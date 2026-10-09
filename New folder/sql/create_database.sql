-- =============================================================
-- create_database.sql
-- Hospital Readmission Analysis - database setup
--
-- Creates the project database, 3 lookup tables (with their data)
-- and the main table that will hold the 101,766 hospital visits.
-- =============================================================

-- 1. Create a fresh database for the project
DROP DATABASE IF EXISTS hospital_readmission;
CREATE DATABASE hospital_readmission
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE hospital_readmission;


-- -------------------------------------------------------------
-- 2. Lookup tables
--    The main data stores ID numbers (e.g. admission_type_id = 1).
--    These tables translate each ID into a readable description.
--    Source: IDs_mapping.csv that comes with the dataset.
-- -------------------------------------------------------------

CREATE TABLE admission_types (
    admission_type_id   INT          PRIMARY KEY,
    description         VARCHAR(150) NOT NULL
);

INSERT INTO admission_types (admission_type_id, description) VALUES
    (1, 'Emergency'),
    (2, 'Urgent'),
    (3, 'Elective'),
    (4, 'Newborn'),
    (5, 'Not Available'),
    (6, 'NULL'),
    (7, 'Trauma Center'),
    (8, 'Not Mapped');


CREATE TABLE discharge_dispositions (
    discharge_disposition_id  INT          PRIMARY KEY,
    description               VARCHAR(150) NOT NULL
);

INSERT INTO discharge_dispositions (discharge_disposition_id, description) VALUES
    (1, 'Discharged to home'),
    (2, 'Discharged/transferred to another short term hospital'),
    (3, 'Discharged/transferred to SNF'),
    (4, 'Discharged/transferred to ICF'),
    (5, 'Discharged/transferred to another type of inpatient care institution'),
    (6, 'Discharged/transferred to home with home health service'),
    (7, 'Left AMA'),
    (8, 'Discharged/transferred to home under care of Home IV provider'),
    (9, 'Admitted as an inpatient to this hospital'),
    (10, 'Neonate discharged to another hospital for neonatal aftercare'),
    (11, 'Expired'),
    (12, 'Still patient or expected to return for outpatient services'),
    (13, 'Hospice / home'),
    (14, 'Hospice / medical facility'),
    (15, 'Discharged/transferred within this institution to Medicare approved swing bed'),
    (16, 'Discharged/transferred/referred another institution for outpatient services'),
    (17, 'Discharged/transferred/referred to this institution for outpatient services'),
    (18, 'NULL'),
    (19, 'Expired at home. Medicaid only, hospice.'),
    (20, 'Expired in a medical facility. Medicaid only, hospice.'),
    (21, 'Expired, place unknown. Medicaid only, hospice.'),
    (22, 'Discharged/transferred to another rehab fac including rehab units of a hospital .'),
    (23, 'Discharged/transferred to a long term care hospital.'),
    (24, 'Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare.'),
    (25, 'Not Mapped'),
    (26, 'Unknown/Invalid'),
    (27, 'Discharged/transferred to a federal health care facility.'),
    (28, 'Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital'),
    (29, 'Discharged/transferred to a Critical Access Hospital (CAH).'),
    (30, 'Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere');


CREATE TABLE admission_sources (
    admission_source_id  INT          PRIMARY KEY,
    description          VARCHAR(150) NOT NULL
);

INSERT INTO admission_sources (admission_source_id, description) VALUES
    (1, 'Physician Referral'),
    (2, 'Clinic Referral'),
    (3, 'HMO Referral'),
    (4, 'Transfer from a hospital'),
    (5, 'Transfer from a Skilled Nursing Facility (SNF)'),
    (6, 'Transfer from another health care facility'),
    (7, 'Emergency Room'),
    (8, 'Court/Law Enforcement'),
    (9, 'Not Available'),
    (10, 'Transfer from critial access hospital'),
    (11, 'Normal Delivery'),
    (12, 'Premature Delivery'),
    (13, 'Sick Baby'),
    (14, 'Extramural Birth'),
    (15, 'Not Available'),
    (17, 'NULL'),
    (18, 'Transfer From Another Home Health Agency'),
    (19, 'Readmission to Same Home Health Agency'),
    (20, 'Not Mapped'),
    (21, 'Unknown/Invalid'),
    (22, 'Transfer from hospital inpt/same fac reslt in a sep claim'),
    (23, 'Born inside this hospital'),
    (24, 'Born outside this hospital'),
    (25, 'Transfer from Ambulatory Surgery Center'),
    (26, 'Transfer from Hospice');


-- -------------------------------------------------------------
-- 3. Main table: one row = one hospital visit (encounter)
--
--    Notes on column names:
--    * Hyphens are replaced by underscores
--      (glyburide-metformin -> glyburide_metformin).
--    * "change" is a reserved word in MySQL, so it is renamed
--      to med_change. A1Cresult -> a1c_result,
--      diabetesMed -> diabetes_med.
--    * '?' in the CSV (missing value) is stored as NULL.
-- -------------------------------------------------------------

CREATE TABLE patient_encounters (
    encounter_id              INT          PRIMARY KEY,
    patient_nbr               INT          NOT NULL,
    race                      VARCHAR(30),
    gender                    VARCHAR(20),
    age                       VARCHAR(10),          -- age band, e.g. '[70-80)'
    weight                    VARCHAR(15),
    admission_type_id         INT,
    discharge_disposition_id  INT,
    admission_source_id       INT,
    time_in_hospital          INT,                  -- days
    payer_code                VARCHAR(5),
    medical_specialty         VARCHAR(60),
    num_lab_procedures        INT,
    num_procedures            INT,
    num_medications           INT,
    number_outpatient         INT,                  -- visits in previous year
    number_emergency          INT,                  -- visits in previous year
    number_inpatient          INT,                  -- visits in previous year
    diag_1                    VARCHAR(10),          -- ICD-9 codes
    diag_2                    VARCHAR(10),
    diag_3                    VARCHAR(10),
    number_diagnoses          INT,
    max_glu_serum             VARCHAR(10),          -- glucose test result
    a1c_result                VARCHAR(10),          -- HbA1c test result
    metformin                  VARCHAR(10),
    repaglinide                VARCHAR(10),
    nateglinide                VARCHAR(10),
    chlorpropamide             VARCHAR(10),
    glimepiride                VARCHAR(10),
    acetohexamide              VARCHAR(10),
    glipizide                  VARCHAR(10),
    glyburide                  VARCHAR(10),
    tolbutamide                VARCHAR(10),
    pioglitazone               VARCHAR(10),
    rosiglitazone              VARCHAR(10),
    acarbose                   VARCHAR(10),
    miglitol                   VARCHAR(10),
    troglitazone               VARCHAR(10),
    tolazamide                 VARCHAR(10),
    examide                    VARCHAR(10),
    citoglipton                VARCHAR(10),
    insulin                    VARCHAR(10),
    glyburide_metformin        VARCHAR(10),
    glipizide_metformin        VARCHAR(10),
    glimepiride_pioglitazone   VARCHAR(10),
    metformin_rosiglitazone    VARCHAR(10),
    metformin_pioglitazone     VARCHAR(10),
    med_change                VARCHAR(5),           -- 'Ch' or 'No'
    diabetes_med              VARCHAR(5),           -- 'Yes' or 'No'
    readmitted                VARCHAR(5)            -- '<30', '>30', 'NO'
);

-- Indexes make filtering / grouping on these columns faster
CREATE INDEX idx_patient     ON patient_encounters (patient_nbr);
CREATE INDEX idx_readmitted  ON patient_encounters (readmitted);
CREATE INDEX idx_age         ON patient_encounters (age);
