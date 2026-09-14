/* ---------------------------------------------------------------------
   Q1. Get all customers whose first name starts with 'J' and who are
       active.
   -----------------------------------------------------------------
   CONCEPT: LIKE with a wildcard, and combining two conditions with AND.
   - 'J%' means "starts with J, followed by anything (%  = any number
     of characters)".
   - active = 1 is a flag column in Sakila (1 = active customer).
   - AND means BOTH conditions must be true for a row to be returned.
   --------------------------------------------------------------------- */
SELECT *
FROM customer
WHERE first_name LIKE 'J%'
  AND active = 1;


/* ---------------------------------------------------------------------
   Q2. Find all films where the title contains 'ACTION' OR the
       description contains 'WAR'.
   -----------------------------------------------------------------
   CONCEPT: LIKE with wildcards on BOTH sides ('%WORD%' = "contains"),
   and OR instead of AND (only ONE condition needs to be true).
   --------------------------------------------------------------------- */
SELECT *
FROM film
WHERE title LIKE '%ACTION%'
   OR description LIKE '%WAR%';


/* ---------------------------------------------------------------------
   Q3. List all customers whose last name is NOT 'SMITH' and whose
       first name ends with 'a'.
   -----------------------------------------------------------------*/
SELECT *
FROM customer
WHERE last_name != 'SMITH'
  AND first_name LIKE '%a';


/* ---------------------------------------------------------------------
   Q4. Get all films where rental_rate > 3.0 and replacement_cost is
       NOT NULL.
   -----------------------------------------------------------------
   CONCEPT: You CANNOT use "= NULL" in SQL (NULL isn't a value you can
   equal, it means "unknown"). You must use IS NULL / IS NOT NULL.
   --------------------------------------------------------------------- */
SELECT *
FROM film
WHERE rental_rate > 3.0
  AND replacement_cost IS not NULL;


/* ---------------------------------------------------------------------
   Q5. Count how many active (active = 1) customers exist in each
       store.
   -----------------------------------------------------------------
   CONCEPT: GROUP BY collapses rows into groups (here, one group per
   store_id) so an aggregate function like COUNT(*) can be applied
   PER GROUP instead of to the whole table.
   - WHERE filters rows BEFORE grouping happens.
   --------------------------------------------------------------------- */
SELECT store_id,
       count(*) AS active_customer_count
FROM customer
WHERE active = 1
GROUP BY store_id;


/* ---------------------------------------------------------------------
   Q6. Show distinct film ratings available in the film table.
   -----------------------------------------------------------------
   CONCEPT: DISTINCT removes duplicate values, returning each unique
   value only once.
   --------------------------------------------------------------------- */
SELECT DISTINCT rating
FROM film;


/* ---------------------------------------------------------------------
   Q7. Find the number of films for each rental duration where the
       AVERAGE length is more than 100 minutes.
   -----------------------------------------------------------------
   CONCEPT: HAVING vs WHERE.
   - WHERE filters individual rows BEFORE grouping.
   - HAVING filters GROUPS AFTER aggregation (you can't write
     "WHERE AVG(length) > 100" because WHERE runs before AVG() is
     calculated -- HAVING is specifically for filtering on aggregates).
   --------------------------------------------------------------------- */
select rental_duration from film ;
SELECT rental_duration,
       COUNT(*)      AS film_count,
       AVG(length)   AS avg_length
FROM film
GROUP BY rental_duration
HAVING AVG(length) > 100;


/* ---------------------------------------------------------------------
   Q8. List payment dates and total amount paid per date, but only
       include days where more than 100 payments were made.
   -----------------------------------------------------------------
   CONCEPT: Combines GROUP BY + HAVING + an aggregate on a DATE part.
   - payment_date is usually a DATETIME (has a time component), so we
     use DATE(payment_date) to strip the time and group by day only.
   - SUM() adds up the amount column per group.
   - HAVING COUNT(*) > 100 filters to only the busy days.
   --------------------------------------------------------------------- */
SELECT DATE(payment_date) AS payment_day,
       SUM(amount)        AS total_amount,
       COUNT(*)           AS payment_count
FROM payment
GROUP BY DATE(payment_date)
HAVING COUNT(*) >= 100;


/* ---------------------------------------------------------------------
   Q9. Find customers whose email is NULL or ends with '.org'.
   -----------------------------------------------------------------
   CONCEPT: Combining IS NULL with LIKE using OR.
   --------------------------------------------------------------------- */
SELECT *
FROM customer
WHERE email IS NULL
   or email LIKE '%.org';


/* ---------------------------------------------------------------------
   Q10. List all films with rating 'PG' or 'G', ordered by rental rate
        descending.
   -----------------------------------------------------------------
   CONCEPT: IN() is shorthand for multiple OR conditions on the SAME
   column ("rating = 'PG' OR rating = 'G'"). ORDER BY ... DESC sorts
   from highest to lowest.
   --------------------------------------------------------------------- */
SELECT *
FROM film
WHERE rating = 'PG' OR rating = 'G'
ORDER BY rental_rate DESC;


/* ---------------------------------------------------------------------
   Q11. Count how many films exist for each length where the film
        title starts with 'T', and the count is more than 5.
   -----------------------------------------------------------------
   CONCEPT: Filter rows first with WHERE (title starts with T), THEN
   group by length, THEN filter the resulting groups with HAVING.
   Order of execution: WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY.
   --------------------------------------------------------------------- */
SELECT length,
       COUNT(*) AS film_count
FROM film
WHERE title LIKE 'T%'
GROUP BY length
HAVING COUNT(*) > 5;


/* ---------------------------------------------------------------------
   Q12. List all actors who have appeared in more than 10 films.
   -----------------------------------------------------------------
   CONCEPT: JOIN + GROUP BY + HAVING.
   - actor and film have a MANY-TO-MANY relationship, linked through
     the bridge table film_actor (which has actor_id and film_id).
   - We JOIN actor to film_actor to count films per actor.
   --------------------------------------------------------------------- */
SELECT a.actor_id,
       a.first_name,
       a.last_name,
       COUNT(fa.film_id) AS film_count
FROM actor a
JOIN film_actor fa
     ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, a.first_name, a.last_name
HAVING COUNT(fa.film_id) > 10;


/* ---------------------------------------------------------------------
   Q13. Find the top 5 films with the highest rental rates and longest
        lengths combined, ordering by rental rate first, then length.
   -----------------------------------------------------------------
   CONCEPT: ORDER BY can take multiple columns -- it sorts by the first
   column, and only uses the second column to break TIES in the first.
   LIMIT restricts the result set to a fixed number of rows (used here
   AFTER sorting, so we get the "top" rows).
   --------------------------------------------------------------------- */
SELECT title,
       rental_rate,
       length
FROM film
ORDER BY rental_rate DESC,
         length DESC
LIMIT 5;


/* ---------------------------------------------------------------------
   Q14. Show all customers along with the total number of rentals they
        have made, ordered from most to least rentals.
   -----------------------------------------------------------------
   CONCEPT: LEFT JOIN (not INNER JOIN!) so that customers with ZERO
   rentals still appear in the result (with a count of 0), instead of
   being excluded. COUNT(r.rental_id) counts only non-NULL rental_ids,
   which correctly gives 0 for customers with no matching rentals.
   --------------------------------------------------------------------- */
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       COUNT(r.rental_id) AS total_rentals
FROM customer c
LEFT JOIN rental r
     ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_rentals DESC;


/* ---------------------------------------------------------------------
   Q15. List the film titles that have never been rented.
   -----------------------------------------------------------------
   CONCEPT: Two common approaches -- a subquery with NOT IN, or a
   LEFT JOIN with a NULL check. Both are shown so you can compare them.

   Path: film -> inventory (each physical copy of a film) -> rental
   (each time a copy was rented out). A film with NO rows in rental
   (via inventory) has never been rented.
   --------------------------------------------------------------------- */

-- Approach A: subquery with NOT IN
SELECT title
FROM film
WHERE film_id NOT IN (
    SELECT i.film_id
    FROM inventory i
    JOIN rental r ON i.inventory_id = r.inventory_id
);

-- Approach B: LEFT JOIN + check for NULL (often more efficient)
SELECT f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
LEFT JOIN rental r ON i.inventory_id = r.inventory_id
WHERE r.rental_id IS NULL;
