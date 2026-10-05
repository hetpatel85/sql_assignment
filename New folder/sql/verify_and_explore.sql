-- =============================================================
-- verify_and_explore.sql
-- Run in MySQL Workbench AFTER load_data.py has finished.
-- Part A checks the load worked (Workflow Step 3).
-- Part B shows a few analysis questions answered with SQL alone.
-- =============================================================

USE hospital_readmission;

-- -------------------------------------------------------------
-- PART A: Verify the load
-- -------------------------------------------------------------

-- A1. Row count (expected: 101766)
SELECT COUNT(*) AS total_rows FROM patient_encounters;

-- A2. Sample rows
SELECT * FROM patient_encounters LIMIT 10;

-- A3. NULL checks on columns that have missing values
SELECT
    SUM(race IS NULL)              AS race_nulls,
    SUM(weight IS NULL)            AS weight_nulls,
    SUM(payer_code IS NULL)        AS payer_code_nulls,
    SUM(medical_specialty IS NULL) AS specialty_nulls,
    SUM(diag_1 IS NULL)            AS diag_1_nulls,
    SUM(diag_2 IS NULL)            AS diag_2_nulls,
    SUM(diag_3 IS NULL)            AS diag_3_nulls
FROM patient_encounters;

-- A4. Duplicate check on the primary key (expected: 0 rows)
SELECT encounter_id, COUNT(*) AS n
FROM patient_encounters
GROUP BY encounter_id
HAVING n > 1;

-- A5. How many unique patients? (some patients visited many times)
SELECT COUNT(DISTINCT patient_nbr) AS unique_patients FROM patient_encounters;


-- -------------------------------------------------------------
-- PART B: Quick analysis with SQL
-- -------------------------------------------------------------

-- B1. Distribution of the target column
SELECT readmitted,
       COUNT(*) AS visits,
       ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM patient_encounters), 2) AS pct
FROM patient_encounters
GROUP BY readmitted
ORDER BY visits DESC;

-- B2. 30-day readmission rate by age band
SELECT age,
       COUNT(*) AS visits,
       ROUND(100 * AVG(readmitted = '<30'), 2) AS readmit_30_pct
FROM patient_encounters
GROUP BY age
ORDER BY age;

-- B3. JOIN with a lookup table: readmission rate by admission type
SELECT t.description AS admission_type,
       COUNT(*) AS visits,
       ROUND(100 * AVG(e.readmitted = '<30'), 2) AS readmit_30_pct
FROM patient_encounters e
JOIN admission_types t ON e.admission_type_id = t.admission_type_id
GROUP BY t.description
ORDER BY visits DESC;

-- B4. Readmission rate by number of inpatient visits in the previous year
SELECT LEAST(number_inpatient, 5) AS prior_inpatient_visits,   -- 5 means "5 or more"
       COUNT(*) AS visits,
       ROUND(100 * AVG(readmitted = '<30'), 2) AS readmit_30_pct
FROM patient_encounters
GROUP BY prior_inpatient_visits
ORDER BY prior_inpatient_visits;

-- B5. Top 10 discharge destinations and their readmission rate
SELECT d.description AS discharged_to,
       COUNT(*) AS visits,
       ROUND(100 * AVG(e.readmitted = '<30'), 2) AS readmit_30_pct
FROM patient_encounters e
JOIN discharge_dispositions d
     ON e.discharge_disposition_id = d.discharge_disposition_id
GROUP BY d.description
ORDER BY visits DESC
LIMIT 10;
