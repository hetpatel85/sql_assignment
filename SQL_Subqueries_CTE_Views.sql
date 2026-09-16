/* =====================================================================
   SUBQUERIES, CTEs, AND VIEWS - LEARNING FILE
   =====================================================================
   Based on the Sakila sample database.
   Run:  USE sakila;   before anything else.

   TOPICS COVERED (in order):
     1. Scalar Subquery        (returns ONE value)
     2. Multi-row Subquery     (returns a LIST of values - used with IN)
     3. Derived Table          (subquery inside FROM, needs an alias)
     4. Correlated Subquery    (inner query depends on the outer row)
     5. CTE (WITH clause)      (named, readable version of a derived table)
     6. Recursive CTE          (a CTE that references itself)
     7. Views                  (a saved query you can SELECT from like a table)
   ===================================================================== */

USE sakila;


/* =====================================================================
   1. SCALAR SUBQUERY
   -----------------------------------------------------------------
   Returns exactly ONE row, ONE column -- a single value. You can use
   it anywhere a single value is expected: after =, >, <, etc.

   GOAL: Find all films that are MORE EXPENSIVE than the average
   rental rate.
   -----------------------------------------------------------------
   HOW IT RUNS: MySQL first runs the inner query
   (SELECT AVG(rental_rate) FROM film) ONCE, gets back a single number
   (say, 2.98), then plugs that number in, effectively running:
       WHERE rental_rate > 2.98
   ===================================================================== */
SELECT title, rental_rate
FROM film
WHERE rental_rate > (SELECT AVG(rental_rate) FROM film)
ORDER BY rental_rate DESC;


/* =====================================================================
   2. MULTI-ROW SUBQUERY (used with IN)
   -----------------------------------------------------------------
   Returns a LIST of values (many rows, one column). You use IN to
   check if a value exists anywhere in that list.

   GOAL: Find all customers who have made at least one payment of
   more than $10 (i.e. customer_id appears in a list of "big spenders").
   -----------------------------------------------------------------
   HOW IT RUNS: The inner query runs first and produces a list like
   (5, 12, 47, 88, ...). The outer query then checks each customer's
   ID against that list.
   ===================================================================== */
SELECT customer_id, first_name, last_name
FROM customer
WHERE customer_id IN (
    SELECT customer_id
    FROM payment
    WHERE amount > 10
);


/* =====================================================================
   3. DERIVED TABLE (subquery inside FROM)
   -----------------------------------------------------------------
   A subquery placed in the FROM clause is treated like a temporary,
   throwaway table. It MUST have an alias (a name) so the outer query
   can refer to it.

   GOAL: Find customers whose total spending exceeds $100.
   -----------------------------------------------------------------
   HOW IT RUNS: The inner query runs FIRST, building a small temporary
   result set (customer_id + their total spend). The outer query then
   treats that result set exactly like a real table called "spending".
   ===================================================================== */
SELECT spending.customer_id, spending.total_spent
FROM (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
) AS spending
WHERE spending.total_spent > 100
ORDER BY spending.total_spent DESC;


/* =====================================================================
   4. CORRELATED SUBQUERY
   -----------------------------------------------------------------
   The inner query references a column from the OUTER query (here,
   f.rating). This means the inner query can't run just once -- it has
   to re-run separately FOR EVERY ROW of the outer query, using that
   row's rating each time. This makes it slower than the other types,
   but sometimes it's the clearest way to express "compare this row
   to others LIKE it."

   GOAL: Find films that are more expensive than the average rental
   rate WITHIN THEIR OWN RATING CATEGORY (not the overall average).
   -----------------------------------------------------------------
   HOW IT RUNS (conceptually, like a loop):
     - Take film #1, say its rating is 'PG'.
       -> Run: SELECT AVG(rental_rate) FROM film WHERE rating = 'PG'
       -> Compare film #1's rate to that PG average.
     - Take film #2, say its rating is 'R'.
       -> Run: SELECT AVG(rental_rate) FROM film WHERE rating = 'R'
       -> Compare film #2's rate to that R average.
     - ...and so on for every row.
   ===================================================================== */
SELECT f.title, f.rating, f.rental_rate
FROM film f
WHERE f.rental_rate > (
    SELECT AVG(f2.rental_rate)
    FROM film f2
    WHERE f2.rating = f.rating   -- <-- this is the "correlation":
                                 --     it links back to the outer row
);


/* =====================================================================
   5. CTE - COMMON TABLE EXPRESSION (the WITH clause)
   -----------------------------------------------------------------
   A CTE is basically the SAME IDEA as a derived table (#3 above), but
   written more readably: you name it up front with WITH, then use
   that name like a normal table in the query below it.

   GOAL: Same as #3 (customers who spent more than $100) but written
   as a CTE instead of a derived table -- compare the readability.
   -----------------------------------------------------------------
   HOW IT RUNS: MySQL runs the WITH block first (naming the result
   "customer_spending"), then runs the final SELECT as if
   "customer_spending" were a real table.
   ===================================================================== */
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
)
SELECT customer_id, total_spent
FROM customer_spending
WHERE total_spent > 100
ORDER BY total_spent DESC;


-- CTEs really shine when you chain MULTIPLE steps together, each
-- building on the last -- this would be very messy as nested derived
-- tables (subqueries inside subqueries inside subqueries).
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
),
big_spenders AS (
    SELECT customer_id
    FROM customer_spending
    WHERE total_spent > 100
)
SELECT c.customer_id, c.first_name, c.last_name, cs.total_spent
FROM customer c
JOIN big_spenders bs ON c.customer_id = bs.customer_id
JOIN customer_spending cs ON c.customer_id = cs.customer_id
ORDER BY cs.total_spent DESC;


/* =====================================================================
   6. RECURSIVE CTE
   -----------------------------------------------------------------
   A recursive CTE is a CTE that refers to ITSELF, used to build up
   results level-by-level (hierarchies, number sequences, date ranges).
   It has two parts, joined by UNION ALL:
     - The ANCHOR: the starting point (runs once).
     - The RECURSIVE part: refers back to the CTE's own name, and
       keeps running, using the PREVIOUS round's results, until it
       produces no more new rows.

   GOAL: Generate a simple sequence of numbers 1 through 10.
   (Sakila doesn't have a natural hierarchy table like "employees
   reporting to managers", so this classic number-generator example
   demonstrates the recursion mechanic clearly without needing one.)
   -----------------------------------------------------------------
   HOW IT RUNS:
     Round 0 (anchor):       n = 1
     Round 1 (recursive):    take n=1, produce n=2
     Round 2 (recursive):    take n=2, produce n=3
     ...
     Stops when the WHERE condition (n < 10) is no longer true.
   ===================================================================== */
WITH RECURSIVE number_sequence AS (
    SELECT 1 AS n                          -- ANCHOR: the starting row
    UNION ALL
    SELECT n + 1                           -- RECURSIVE: build on the previous row
    FROM number_sequence
    WHERE n < 10                           -- stop condition
)
SELECT n
FROM number_sequence;

-- A more "database-flavored" recursive example: generate every date
-- from the earliest to the latest payment date in Sakila.
WITH RECURSIVE date_range AS (
    SELECT MIN(DATE(payment_date)) AS a_date FROM payment    -- ANCHOR
    UNION ALL
    SELECT DATE_ADD(a_date, INTERVAL 1 DAY)                  -- RECURSIVE
    FROM date_range
    WHERE a_date < (SELECT MAX(DATE(payment_date)) FROM payment)
)
SELECT a_date
FROM date_range
LIMIT 20;   -- limited here just so it doesn't print hundreds of rows


/* =====================================================================
   7. VIEWS
   -----------------------------------------------------------------
   A VIEW is a SAVED query that behaves like a virtual table. It does
   NOT store data itself -- every time you SELECT from it, the
   underlying query runs fresh, live, against the real tables.

   Why use one? To save a complex query (like our big_spenders logic
   above) under a simple, reusable name, so you (or teammates) don't
   have to rewrite the JOIN/GROUP BY logic every time.

   GOAL: Turn the "customer spending" logic from #5 into a reusable view.
   ===================================================================== */

-- Step 1: create the view (run this once)
CREATE VIEW customer_spending_view AS
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       SUM(p.amount) AS total_spent
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- Step 2: now use it just like a normal table, any time, in any query
SELECT *
FROM customer_spending_view
WHERE total_spent > 100
ORDER BY total_spent DESC;

-- You can even filter/join it further, same as a real table:
SELECT first_name, last_name, total_spent
FROM customer_spending_view
WHERE total_spent BETWEEN 50 AND 100;

-- To remove a view you no longer need:
-- DROP VIEW customer_spending_view;
