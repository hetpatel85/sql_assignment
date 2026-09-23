USE sakila;
/* ---------------------------------------------------------------------
   A1. Scalar subquery
       Find all films priced higher than the average rental rate.
   -----------------------------------------------------------------
   The inner query runs ONCE and returns a single number. The outer
   query compares every row against that one fixed value.
   --------------------------------------------------------------------- */
SELECT title, rental_rate
FROM film
WHERE rental_rate > (SELECT AVG(rental_rate) FROM film);


/* ---------------------------------------------------------------------
   A2. Multi-row subquery (IN)
       Find customers who have made more than 5 payments.
   -----------------------------------------------------------------
   The inner query returns a LIST of customer_ids (those with more
   than 5 payments). The outer query keeps any customer whose ID
   appears anywhere in that list.
   --------------------------------------------------------------------- */
SELECT customer_id, first_name, last_name
FROM customer
WHERE customer_id IN (
    SELECT customer_id
    FROM payment
    GROUP BY customer_id
    HAVING COUNT(*) > 5
);


/* ---------------------------------------------------------------------
   A3. Correlated subquery
       Find films priced higher than the average rental rate FOR THEIR
       OWN RATING category (PG films compared only to other PG films,
       R films only to other R films, etc.)
   -----------------------------------------------------------------
   The inner query references f.rating from the OUTER query, so it
   can't run just once -- it re-runs for each rating group, using that
   row's own rating each time. This is what makes it "correlated."
   --------------------------------------------------------------------- */
SELECT f.title, f.rating, f.rental_rate
FROM film f
WHERE f.rental_rate > (
    SELECT AVG(f2.rental_rate)
    FROM film f2
    WHERE f2.rating = f.rating
);

/* ---------------------------------------------------------------------
   B1. Basic CTE
       Find customers who have spent more than $100 in total.
   -----------------------------------------------------------------
   WITH names a query up front (customer_spending). The final SELECT
   below then treats that name exactly like a real table. This is the
   same logic as a derived table, just written top-to-bottom instead
   of nested, which is far easier to read.
   --------------------------------------------------------------------- */
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
)
SELECT customer_id, total_spent
FROM customer_spending
WHERE total_spent > 100
ORDER BY total_spent DESC;


/* ---------------------------------------------------------------------
   B2. Multiple chained CTEs
       Find the names of customers who are "big spenders" (>$100),
       showing their total spent amount too.
   -----------------------------------------------------------------
   You can stack CTEs one after another, separated by commas, where
   each later CTE can use the ones defined before it. Here,
   big_spenders is built directly from customer_spending. Trying to do
   this with nested nested subqueries instead would get messy fast --
   that's the main reason CTEs exist.
   --------------------------------------------------------------------- */
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
),
big_spenders AS (
    SELECT customer_id, total_spent
    FROM customer_spending
    WHERE total_spent > 100
)
SELECT c.customer_id, c.first_name, c.last_name, bs.total_spent
FROM customer c
JOIN big_spenders bs ON c.customer_id = bs.customer_id
ORDER BY bs.total_spent DESC;


/* ---------------------------------------------------------------------
   B3. Recursive CTE
       Generate a simple sequence of numbers from 1 to 10.
   -----------------------------------------------------------------
   A recursive CTE refers to ITSELF. It has two parts joined by
   UNION ALL:
     - ANCHOR: the starting row (n = 1).
     - RECURSIVE part: builds the next row from the previous one
       (n + 1), and keeps going until the WHERE condition stops it.
   Trace it like a loop: n=1 -> produces n=2 -> produces n=3 -> ...
   -> stops once n is no longer less than 10.
   --------------------------------------------------------------------- */
WITH RECURSIVE number_sequence AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1
    FROM number_sequence
    WHERE n < 10
)
SELECT n
FROM number_sequence;



/* ---------------------------------------------------------------------
   C1. Simple view
       Save "customer total spending" as a reusable view.
   --------------------------------------------------------------------- */
CREATE VIEW customer_spending_view AS
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       SUM(p.amount) AS total_spent
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- Using it afterward is just like querying a table:
SELECT *
FROM customer_spending_view
WHERE total_spent > 100
ORDER BY total_spent DESC;


/* ---------------------------------------------------------------------
   C2. View built on a JOIN
       Save a simplified "film catalog" view showing title, category,
       and rental rate together (normally spread across 3 tables:
       film, film_category, category).
   --------------------------------------------------------------------- */
CREATE VIEW film_catalog_view AS
SELECT f.film_id,
       f.title,
       cat.name AS category_name,
       f.rental_rate
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id;

-- Now anyone can get "title + category + price" in one simple query,
-- without needing to remember the underlying 3-table JOIN:
SELECT *
FROM film_catalog_view
WHERE category_name = 'Action'
ORDER BY rental_rate DESC;


/* ---------------------------------------------------------------------
   C3. View with aggregation
       Save a "films per category count" view.
   --------------------------------------------------------------------- */
CREATE VIEW films_per_category_view AS
SELECT cat.name AS category_name,
       COUNT(*) AS film_count
FROM film_category fc
JOIN category cat ON fc.category_id = cat.category_id
GROUP BY cat.name;

-- Use it directly:
SELECT *
FROM films_per_category_view
ORDER BY film_count DESC;


/* =====================================================================
   PART D - TEMPORARY TABLE (1 example)
   -----------------------------------------------------------------
   A TEMP TABLE is different from a view: it actually STORES a real
   copy of data (a snapshot, frozen at the moment you created it), but
   only for the duration of your current session/connection. Once you
   disconnect (or close Workbench), it automatically disappears.

   Why use one instead of a CTE or view?
     - CTEs only live for a single query, then vanish.
     - Views never store data -- they always recalculate live.
     - Temp tables store data ONCE and let you reuse/query/index that
       snapshot repeatedly within your session, which can be faster if
       you need to run several different queries against the same
       intermediate result.
   ===================================================================== */

-- Step 1: create the temp table from a query (runs once, stores results)
CREATE TEMPORARY TABLE temp_customer_spending AS
SELECT customer_id, SUM(amount) AS total_spent
FROM payment
GROUP BY customer_id;

-- Step 2: now query it like any normal table, as many times as you like
SELECT *
FROM temp_customer_spending
WHERE total_spent > 100
ORDER BY total_spent DESC;

-- You can run other, completely different queries against the same
-- snapshot without recalculating anything:
SELECT AVG(total_spent) AS avg_spending
FROM temp_customer_spending;

-- To remove it manually before your session ends (optional -- it
-- disappears automatically once you disconnect anyway):
-- DROP TEMPORARY TABLE temp_customer_spending;