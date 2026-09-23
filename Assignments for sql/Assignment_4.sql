/* ===================
   Based on the Sakila sample database.
   Run:  USE sakila;   before anything else.

   JOIN TYPES USED IN THIS FILE:
     - INNER JOIN  : only rows that match in BOTH tables
     - LEFT JOIN   : all rows from the left table, matched data from
                     the right if it exists, NULL if it doesn't
     - RIGHT JOIN  : mirror image of LEFT JOIN
     - FULL OUTER JOIN : MySQL doesn't support this directly, so we
                     simulate it with LEFT JOIN UNION RIGHT JOIN
   ===================================================================== */

USE sakila;


/* ---------------------------------------------------------------------
   Q1. List all customers along with the films they have rented.
   -----------------------------------------------------------------
   CONCEPT: INNER JOIN chained across 3 tables. A customer connects to
   a film through TWO steps: customer -> rental -> inventory -> film.
   rental tells us WHO rented WHAT inventory item; inventory tells us
   WHICH film that item is a copy of.

   We use INNER JOIN here (not LEFT JOIN) on purpose, because the
   question asks to show customers "along with the films they rented"
   -- if a customer never rented anything, there's nothing to show
   next to their name, so it's fine for them to be excluded.
   --------------------------------------------------------------------- */
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       f.title
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
ORDER BY c.customer_id;


/* ---------------------------------------------------------------------
   Q2. List all customers and show their rental count, INCLUDING those
       who haven't rented any films.
   -----------------------------------------------------------------
   CONCEPT: LEFT JOIN, not INNER JOIN. The phrase "including those who
   haven't rented any" is the signal -- an INNER JOIN would silently
   drop customers with zero rentals, since there'd be nothing to match
   on the right side. LEFT JOIN keeps every customer regardless, and
   fills in NULLs for the missing side, which COUNT() then turns into 0.

   COUNT(r.rental_id) -- not COUNT(*) -- matters here: COUNT(*) would
   count 1 for every customer (even ones with no rentals, since the
   row still technically exists after the LEFT JOIN). COUNT(r.rental_id)
   only counts non-NULL rental_ids, correctly giving 0 for no rentals.
   --------------------------------------------------------------------- */
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       COUNT(r.rental_id) AS rental_count
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY rental_count DESC;


/* ---------------------------------------------------------------------
   Q3. Show all films along with their category. Include films that
       don't have a category assigned.
   -----------------------------------------------------------------
   CONCEPT: LEFT JOIN again, same reasoning as Q2 -- "include films
   that don't have a category" means we can't use INNER JOIN, since
   that would drop any film missing a film_category row entirely.

   film connects to category through the bridge table film_category
   (same many-to-many pattern as actor/film_actor from Q12 earlier).
   --------------------------------------------------------------------- */
SELECT f.title,
       cat.name AS category_name
FROM film f
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category cat ON fc.category_id = cat.category_id
ORDER BY f.title;


/* ---------------------------------------------------------------------
   Q4. Show all customers and staff emails from both customer and
       staff tables using a FULL OUTER JOIN (simulate using LEFT +
       RIGHT + UNION).
   -----------------------------------------------------------------
   CONCEPT: A FULL OUTER JOIN keeps EVERY row from BOTH tables, matching
   them where possible and filling NULLs where there's no match on
   either side. MySQL doesn't have a FULL OUTER JOIN keyword at all --
   so the standard workaround is:
       (LEFT JOIN)  UNION  (RIGHT JOIN)
   The LEFT JOIN captures "everything on the left, plus matches,"
   the RIGHT JOIN captures "everything on the right, plus matches,"
   and UNION combines both sets while automatically removing exact
   duplicate rows (the ones that matched in both directions).

   We join customer and staff on store_id, since that's the one column
   they actually share (both tables record which store someone belongs
   to) -- there's no direct customer-to-staff relationship otherwise.
   --------------------------------------------------------------------- */
SELECT c.customer_id, c.email AS customer_email, s.staff_id, s.email AS staff_email
FROM customer c
LEFT JOIN staff s ON c.store_id = s.store_id

UNION

SELECT c.customer_id, c.email AS customer_email, s.staff_id, s.email AS staff_email
FROM customer c
RIGHT JOIN staff s ON c.store_id = s.store_id;


/* ---------------------------------------------------------------------
   Q5. Find all actors who acted in the film "ACADEMY DINOSAUR".
   -----------------------------------------------------------------
   CONCEPT: INNER JOIN chained through the actor <-> film_actor <-> film
   bridge, filtered down to one specific title with WHERE.
   --------------------------------------------------------------------- */
SELECT a.first_name,
       a.last_name
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN film f ON fa.film_id = f.film_id
WHERE f.title = 'ACADEMY DINOSAUR';


/* ---------------------------------------------------------------------
   Q6. List all stores and the total number of staff members working
       in each store, even if a store has no staff.
   -----------------------------------------------------------------
   CONCEPT: LEFT JOIN starting from the store side this time (store is
   the "keep everything" table), then COUNT() + GROUP BY as usual.
   Same COUNT(column) vs COUNT(*) reasoning as Q2 applies here.
   --------------------------------------------------------------------- */
SELECT st.store_id,
       COUNT(s.staff_id) AS staff_count
FROM store st
LEFT JOIN staff s ON st.store_id = s.store_id
GROUP BY st.store_id;


/* ---------------------------------------------------------------------
   Q7. List the customers who have rented films more than 5 times.
       Include their name and total rental count.
   -----------------------------------------------------------------
   CONCEPT: INNER JOIN (not LEFT, this time) + GROUP BY + HAVING.
   INNER JOIN is correct here because customers with ZERO rentals could
   never have "more than 5" anyway -- they'd be filtered out by HAVING
   regardless, so there's no need to keep them around with a LEFT JOIN.
   --------------------------------------------------------------------- */
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       COUNT(r.rental_id) AS total_rentals
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(r.rental_id) > 5
ORDER BY total_rentals DESC;