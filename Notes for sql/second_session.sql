-- SELECT * : returns ALL columns. Fine for exploring, avoid in real
-- applications (slower and breaks when columns change).
SELECT * FROM sakila.actor;

-- Select only the columns you need (list them separated by commas).
SELECT actor_id, last_name FROM sakila.actor;
SELECT first_name, last_name FROM sakila.actor;

/* =====================================================================
   SECTION 2: DISTINCT (REMOVE DUPLICATES)
   ===================================================================== */

-- DISTINCT returns each different value only once.
-- Many actors share a first name, so this list is shorter than the table.
SELECT DISTINCT first_name FROM sakila.actor;

-- Distinct values of a column (rating = G, PG, PG-13, R, NC-17).
-- DISTINCT is NOT a function: "DISTINCT rating" and "DISTINCT(rating)"
-- are identical. The parentheses are optional and do nothing special.
SELECT DISTINCT rating FROM sakila.film;

-- DISTINCT over several columns applies to the COMBINATION:
SELECT DISTINCT rating, rental_duration FROM sakila.film;


/* =====================================================================
   SECTION 3: IS NULL / IS NOT NULL
   ---------------------------------------------------------------------
   NULL means "no value / unknown". It is not zero and not an empty string.
   - Use  IS NULL  /  IS NOT NULL
   - NEVER use  = NULL  (it is never true)
   ===================================================================== */

-- Films with no original language recorded.
-- (In the standard Sakila data this column is NULL for every film, so this
--  returns all films.)
SELECT * FROM sakila.film WHERE original_language_id IS NULL;

-- Equality filter
SELECT * FROM sakila.film WHERE rental_duration = 6;

-- COUNT(*) counts rows
SELECT COUNT(*) FROM sakila.film WHERE rental_duration = 6;

-- DISTINCT title vs plain title (titles are unique here, so same result)
SELECT DISTINCT title FROM sakila.film WHERE original_language_id IS NULL;
SELECT title          FROM sakila.film WHERE original_language_id IS NULL;


/* =====================================================================
   SECTION 4: COUNT AND DISTINCT COUNT
   ---------------------------------------------------------------------
   COUNT(*)               -> counts all rows (including NULLs)
   COUNT(column)          -> counts rows where column is NOT NULL
   COUNT(DISTINCT column) -> counts different non-NULL values
   ===================================================================== */

-- Number of different film titles
SELECT COUNT(DISTINCT title) FROM sakila.film;

-- All actor rows with a first name (200 in the sample data)
SELECT COUNT(first_name) FROM sakila.actor;

-- Number of DIFFERENT first names (smaller, because of duplicates)
SELECT COUNT(DISTINCT first_name) FROM sakila.actor;

-- Find duplicated first names: group, then keep groups with more than 1 row
SELECT first_name, COUNT(first_name) AS times_used
FROM sakila.actor
GROUP BY first_name
HAVING COUNT(first_name) > 1;

-- Look at one of the duplicated names
SELECT * FROM sakila.actor WHERE first_name = 'PENELOPE';

/* =====================================================================
   SECTION 6: FILTERING WITH WHERE
   ---------------------------------------------------------------------
   Comparison operators:  =   !=  (or <>)   >   <   >=   <=
   ===================================================================== */

-- Text values go in single quotes; numbers do not.
-- Both conditions must be true (AND).
SELECT * FROM sakila.film WHERE rating = 'R' AND length >= 92;

-- Only one condition
SELECT * FROM sakila.film WHERE length >= 92;


/* =====================================================================
   SECTION 7: SORTING WITH ORDER BY
   ---------------------------------------------------------------------
   ORDER BY column ASC   -> smallest to largest / A to Z  (DEFAULT)
   ORDER BY column DESC  -> largest to smallest / Z to A
   ===================================================================== */

SELECT rental_rate FROM sakila.film;

-- Most expensive rentals first
SELECT title, rental_rate FROM sakila.film ORDER BY rental_rate DESC;

-- Sort by several columns: first by rate (high to low), ties by title (A-Z)
SELECT title, rental_rate FROM sakila.film ORDER BY rental_rate DESC, title ASC;


/* =====================================================================
   SECTION 8: AND, OR, NOT
   ---------------------------------------------------------------------
   AND -> ALL conditions must be true
   OR  -> AT LEAST ONE condition must be true
   NOT -> reverses a condition
   Precedence: NOT, then AND, then OR. Use parentheses to be clear.
   ===================================================================== */

-- AND: rating PG *and* 5 days
SELECT * FROM sakila.film
WHERE rating = 'PG' AND rental_duration = 5
ORDER BY rental_rate ASC;

-- OR: rating PG *or* 5 days (returns more rows than AND)
SELECT * FROM sakila.film
WHERE rating = 'PG' OR rental_duration = 5
ORDER BY rental_rate ASC;

-- NOT IN: exclude a list of values
SELECT * FROM sakila.film
WHERE rental_duration NOT IN (6, 7, 3)
ORDER BY rental_rate ASC;

-- Three ways to say "not equal to 6". All give the same result:
SELECT * FROM sakila.film WHERE NOT rental_duration = 6  ORDER BY rental_rate ASC;
SELECT * FROM sakila.film WHERE rental_duration != 6     ORDER BY rental_rate ASC;
SELECT * FROM sakila.film WHERE rental_duration <> 6     ORDER BY rental_rate ASC;

-- PARENTHESES CHANGE THE MEANING.
-- With parentheses: duration 6 AND (G or PG)
SELECT * FROM sakila.film
WHERE rental_duration = 6 AND (rating = 'G' OR rating = 'PG')
ORDER BY rental_rate ASC;

-- Without parentheses AND runs first, so this means:
-- (duration 6 AND G)  OR  PG   -> a different (wrong) result
SELECT * FROM sakila.film
WHERE rental_duration = 6 AND rating = 'G' OR rating = 'PG'
ORDER BY rental_rate ASC;

-- IN is a shorter way to write several ORs on the same column:
SELECT * FROM sakila.film
WHERE rental_duration = 6 AND rating IN ('G', 'PG')
ORDER BY rental_rate ASC;


/* =====================================================================
   SECTION 9: LIKE (PATTERN MATCHING)
   ---------------------------------------------------------------------
   Two wildcards:
     %  -> zero, one or many characters
     _  -> exactly ONE character
   Examples:
     'a%'     starts with a
     '%a'     ends with a
     '%a%'    contains a
     '_a%'    second letter is a
     'a_%_%'  starts with a and is at least 3 characters long
   In MySQL, LIKE is case-insensitive by default.
   ===================================================================== */

-- Cities ending with "a"
SELECT city FROM sakila.city WHERE city LIKE '%a';

-- Ratings containing "PG" (matches PG and PG-13)
SELECT rating FROM sakila.film WHERE rating LIKE '%PG%';

-- Pattern '_a___s%' means:
--   _    any 1st character
--   a    2nd character is "a"
--   ___  any 3 characters (3rd, 4th, 5th)
--   s    6th character is "s"
--   %    anything after
SELECT city FROM sakila.city WHERE city LIKE '_a___s%';

-- More examples (were commented out in the original):
SELECT title FROM sakila.film WHERE title LIKE '%super%';   -- contains "super"
SELECT title FROM sakila.film WHERE title LIKE '__s_s%';    -- 3rd letter s, 5th letter s

-- NOT LIKE excludes matches
SELECT DISTINCT rating FROM sakila.film WHERE rating NOT LIKE '%PG%';


/* =====================================================================
   SECTION 10: NULL VALUES IN PRACTICE
   ===================================================================== */

-- Look at the whole rental table first
SELECT * FROM sakila.rental;

-- Rentals that were never returned (return_date is NULL)
SELECT rental_id, inventory_id, customer_id, return_date
FROM sakila.rental
WHERE return_date IS NULL;

-- Rentals that WERE returned
SELECT rental_id, inventory_id, customer_id, return_date
FROM sakila.rental
WHERE return_date IS NOT NULL;

-- [WRONG] "= NULL" never matches anything, it returns 0 rows:
-- SELECT * FROM sakila.rental WHERE return_date = NULL;


/* =====================================================================
   SECTION 11: BETWEEN
   ---------------------------------------------------------------------
   BETWEEN a AND b is INCLUSIVE: it includes both a and b.
   It is the same as:  >= a AND <= b
   Works with numbers, text and dates.
   ===================================================================== */

SELECT rental_id, inventory_id, customer_id, return_date
FROM sakila.rental
WHERE return_date BETWEEN '2005-05-26' AND '2005-05-30';

-- WATCH OUT with DATETIME columns: '2005-05-30' means 2005-05-30 00:00:00,
-- so returns later on May 30th are NOT included. To include the whole day:
SELECT rental_id, inventory_id, customer_id, return_date
FROM sakila.rental
WHERE return_date >= '2005-05-26'
  AND return_date <  '2005-05-31';

-- Numbers example: films between 90 and 120 minutes (both included)
SELECT title, length FROM sakila.film WHERE length BETWEEN 90 AND 120;


/* =====================================================================
   SECTION 12: AGGREGATE FUNCTIONS (needed for GROUP BY)
   ---------------------------------------------------------------------
   COUNT()  number of rows        SUM()  total
   AVG()    average               MIN()  smallest
   MAX()    largest
   Aggregate functions ignore NULL values (except COUNT(*)).
   ===================================================================== */

SELECT COUNT(*)    AS total_payments,
       SUM(amount) AS total_amount,
       AVG(amount) AS average_amount,
       MIN(amount) AS smallest,
       MAX(amount) AS largest
FROM sakila.payment;


/* =====================================================================
   SECTION 13: GROUP BY AND HAVING
   ---------------------------------------------------------------------
   GROUP BY : puts rows with the same value(s) into groups, so you can
              run an aggregate function (COUNT, SUM...) on each group.
   HAVING   : filters the GROUPS after they are made.
   Rule: every column in SELECT must either be in GROUP BY or be inside
         an aggregate function.
   ===================================================================== */

-- For unreturned rentals, count how many rentals each customer made at
-- each exact rental_date/time, keep groups with fewer than 30,
-- show the biggest first, limit to 50 rows.
SELECT customer_id,
       rental_date,
       COUNT(rental_id) AS count_rentals
FROM sakila.rental
WHERE return_date IS NULL
GROUP BY customer_id, rental_date
HAVING COUNT(rental_id) < 30
ORDER BY count_rentals DESC
LIMIT 50;

-- NOTE ON "FINDING DUPLICATES": to find duplicates you keep groups that
-- have MORE THAN ONE row, so use  HAVING COUNT(...) > 1.
-- "< 30" (as in the query above) keeps almost every group, so it does not
-- really check duplicates. Duplicate check template:
--   SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > 1;
SELECT customer_id, rental_date, COUNT(rental_id) AS count_rentals
FROM sakila.rental
GROUP BY customer_id, rental_date
HAVING COUNT(rental_id) > 1;

-- Look at the rows of one customer
SELECT * FROM sakila.rental WHERE customer_id = 168;
SELECT * FROM sakila.rental;

-- Total number of rental rows
SELECT COUNT(*) AS count FROM sakila.rental;


/* =====================================================================
   SECTION 14: ORDER OF EXECUTION IN SQL
   ---------------------------------------------------------------------
   The order you WRITE a query is NOT the order MySQL RUNS it.

   WRITTEN ORDER:   SELECT -> FROM -> JOIN -> WHERE -> GROUP BY
                    -> HAVING -> ORDER BY -> LIMIT

   EXECUTION ORDER:
     1. FROM      (pick the table)
     2. JOIN      (combine tables)
     3. WHERE     (filter individual rows)
     4. GROUP BY  (make groups)
     5. HAVING    (filter groups)
     6. SELECT    (choose columns / calculate aliases)
     7. DISTINCT  (remove duplicates)
     8. ORDER BY  (sort)
     9. LIMIT     (cut the number of rows)

   WHY IT MATTERS:
   - You can use a column alias in ORDER BY (it runs after SELECT).
   - You can NOT use an alias in WHERE (WHERE runs before SELECT).
   ===================================================================== */

-- Alias used in ORDER BY: works
SELECT customer_id, SUM(amount) AS total_payment
FROM sakila.payment
GROUP BY customer_id
ORDER BY total_payment DESC
LIMIT 5;


/* =====================================================================
   SECTION 15: DIFFERENCE BETWEEN WHERE AND HAVING
   ---------------------------------------------------------------------
   | WHERE                         | HAVING                          |
   |-------------------------------|---------------------------------|
   | Filters ROWS                  | Filters GROUPS                  |
   | Runs BEFORE GROUP BY          | Runs AFTER GROUP BY             |
   | Cannot use aggregates         | Can use aggregates (SUM, COUNT) |
   |   (e.g. SUM(amount) > 100)    |                                 |
   | Faster (fewer rows to group)  | Use only for aggregate filters  |
   ===================================================================== */

-- WHERE: filter rows (only unreturned rentals)
SELECT * FROM sakila.rental WHERE return_date IS NULL;

-- WHERE: filter rows of one customer
SELECT * FROM sakila.rental WHERE customer_id = 33;

-- Look at the payment table
SELECT * FROM sakila.payment;

-- WHERE + HAVING together: total payment per customer.
-- Customers 1 to 100 whose total payments are above 100.
SELECT customer_id, SUM(amount) AS total_payment
FROM sakila.payment
GROUP BY customer_id
HAVING SUM(amount) > 100 AND customer_id BETWEEN 1 AND 100;

-- BETTER VERSION: a condition on a plain column (customer_id) belongs in
-- WHERE. It filters rows BEFORE grouping, so MySQL does less work.
-- Only the aggregate condition (SUM) stays in HAVING. Same result.
SELECT customer_id, SUM(amount) AS total_payment
FROM sakila.payment
WHERE customer_id BETWEEN 1 AND 100
GROUP BY customer_id
HAVING SUM(amount) > 100;

