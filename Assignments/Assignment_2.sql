SELECT first_name,
       last_name,
       email,
       COUNT(*) AS occurrences
FROM customer
GROUP BY first_name, last_name, email
HAVING COUNT(*) > 1;

/* Q2. Number of times the letter 'a' is repeated in film descriptions
       (across ALL descriptions combined).*/
       
SELECT SUM(
         LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'a', ''))
       ) AS total_a_count
FROM film;


/* ---------------------------------------------------------------------
   Q3. Number of times EACH vowel is repeated in film descriptions.
   -----------------------------------------------------------------
   CONCEPT: Same LENGTH/REPLACE trick as Q2, just repeated once per
   vowel (a, e, i, o, u), each as its own summed column.
   --------------------------------------------------------------------- */
SELECT
    SUM(LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'a', ''))) AS a_count,
    SUM(LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'e', ''))) AS e_count,
    SUM(LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'i', ''))) AS i_count,
    SUM(LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'o', ''))) AS o_count,
    SUM(LENGTH(LOWER(description)) - LENGTH(REPLACE(LOWER(description), 'u', ''))) AS u_count
FROM film;


/* ---------------------------------------------------------------------
   Q4. Display the payments made by each customer:
       4a. Month wise   4b. Year wise   4c. Week wise
   -----------------------------------------------------------------
   CONCEPT: MONTH(), YEAR(), and WEEK() extract just that piece of a
   date column. Grouping by customer_id + that piece gives totals per
   customer per time bucket.
   --------------------------------------------------------------------- */

-- 4a. Month-wise (grouped by customer + calendar month, across all years)
SELECT customer_id,
       MONTH(payment_date) AS payment_month,
       SUM(amount)         AS total_paid
FROM payment
GROUP BY customer_id, MONTH(payment_date)
ORDER BY customer_id, payment_month;

-- 4b. Year-wise
SELECT customer_id,
       YEAR(payment_date) AS payment_year,
       SUM(amount)        AS total_paid
FROM payment
GROUP BY customer_id, YEAR(payment_date)
ORDER BY customer_id, payment_year;

-- 4c. Week-wise (WEEK() returns the week number within the year, 0-53)
SELECT customer_id,
       YEAR(payment_date) AS payment_year,
       WEEK(payment_date) AS payment_week,
       SUM(amount)        AS total_paid
FROM payment
GROUP BY customer_id, YEAR(payment_date), WEEK(payment_date)
ORDER BY customer_id, payment_year, payment_week;


/* ---------------------------------------------------------------------
   Q5. Check if any given year is a leap year or not.
       (Hardcoded date, no Sakila table involved.)
   -----------------------------------------------------------------
   CONCEPT: The leap year rule is:
     - Divisible by 4   AND
     - NOT divisible by 100, UNLESS it's also divisible by 400
   In SQL, % (or MOD()) gives the remainder of division. remainder = 0
   means "evenly divisible."
   A CASE expression works like if/else logic inside a SELECT.
   --------------------------------------------------------------------- */
SELECT 2026 AS year_to_check,
       CASE
           WHEN 2026 % 4 = 0 AND (2026 % 100 <> 0 OR 2026 % 400 = 0)
               THEN 'Leap Year'
           ELSE 'Not a Leap Year'
       END AS result;
/* ---------------------------------------------------------------------
   Q6. Display number of days remaining in the current year from today.
   -----------------------------------------------------------------
   CONCEPT: CURDATE() returns today's date. DATEDIFF(end, start) returns
   the number of days between two dates. We build "Dec 31 of this year"
   using CONCAT() + YEAR(CURDATE()), then find the gap to today.
   --------------------------------------------------------------------- */
SELECT CURDATE()                                          AS today,
       CONCAT(YEAR(CURDATE()), '-12-31')                  AS year_end,
       DATEDIFF(CONCAT(YEAR(CURDATE()), '-12-31'), CURDATE()) AS days_remaining;


/* ---------------------------------------------------------------------
   Q7. Display quarter number (Q1, Q2, Q3, Q4) for payment dates.
   -----------------------------------------------------------------
   CONCEPT: QUARTER() is a built-in function that returns 1-4 directly
   based on the month (Jan-Mar = 1, Apr-Jun = 2, Jul-Sep = 3, Oct-Dec = 4).
   We prefix it with 'Q' using CONCAT() just to match the requested
   display format ("Q1", "Q2", etc.) instead of a bare number.
   --------------------------------------------------------------------- */
SELECT payment_id,
       payment_date,
       CONCAT('Q', QUARTER(payment_date)) AS payment_quarter
FROM payment;
