-- DATABASE : an organized collection of data stored electronically.
-- DBMS     : Database Management System - software that creates, stores and
--            manages databases (MySQL, PostgreSQL, Oracle, SQL Server).
-- SQL      : Structured Query Language - the language used to talk to a
--            relational database.
-- SCHEMA   : the blueprint of a database (tables, columns, data types,
--            relationships). In MySQL, SCHEMA and DATABASE are synonyms.
--
-- RDBMS    : Relational DBMS - stores data in tables (rows + columns)
--            and links tables using keys. MySQL is an RDBMS.
--
-- SQL COMMAND CATEGORIES
-- ----------------------
-- DDL - Data Definition Language   : CREATE, ALTER, DROP, TRUNCATE (+ RENAME)
--                                    -> defines/changes STRUCTURE
-- DML - Data Manipulation Language : INSERT, UPDATE, DELETE
--                                    -> changes the DATA
-- DQL - Data Query Language        : SELECT
--                                    -> reads data
-- DCL - Data Control Language      : GRANT, REVOKE
--                                    -> permissions / access
-- TCL - Transaction Control Lang.  : COMMIT, ROLLBACK, SAVEPOINT
--                                    -> saves or undoes changes


/* =====================================================================
   SECTION 2: CREATE DATABASE
   ===================================================================== */

-- Start fresh so the script can be re-run any number of times.
DROP DATABASE IF EXISTS company_db;

-- CREATE DATABASE (DDL): creates an empty database.
CREATE DATABASE company_db;

-- Useful database commands:
SHOW DATABASES;            -- list all databases on the server
-- USE company_db;         -- make company_db the default database. After this
--                         -- you can write "test_table" instead of
--                         -- "company_db.test_table".
-- In this file we always write "company_db.table_name" (fully qualified),
-- so USE is not required.
-- Common data types:
--   INT           whole numbers
--   DECIMAL(p,s)  exact numbers, e.g. DECIMAL(10,2) = 12345678.99 (money)
--   VARCHAR(n)    text up to n characters
--   CHAR(n)       fixed-length text
--   DATE          'YYYY-MM-DD'
--   DATETIME      'YYYY-MM-DD HH:MM:SS'
--   BOOLEAN       TRUE / FALSE (stored as 1 / 0)

CREATE TABLE company_db.test_table (
  id   INT,
  name VARCHAR(100)
);

-- Inspect a table's structure:
DESCRIBE company_db.test_table;           -- columns, types, keys
SHOW TABLES FROM company_db;              -- list tables in the database
SHOW CREATE TABLE company_db.test_table;  -- shows the full CREATE statement

-- Select ONE column
SELECT id FROM company_db.test_table;

-- Select ALL columns ( * = every column ). The table is empty right now.
SELECT * FROM company_db.test_table;
-- Syntax: INSERT INTO table (col1, col2) VALUES (v1, v2), (v3, v4);
-- You can insert several rows in one statement by separating with commas.
INSERT INTO company_db.test_table (id, name)
VALUES
  (1, 'Alice'),
  (2, 'Bob'),
  (3, 'Charlie');

-- Data type conversion: name is VARCHAR, so the number 5 is converted to
-- the text '5'. This WORKS.
INSERT INTO company_db.test_table (id, name)
VALUES (5, 5);

-- [WILL FAIL] 'joey' cannot be converted to INT, so MySQL raises
-- "Incorrect integer value".
-- INSERT INTO company_db.test_table (id, name)
-- VALUES ('joey', 5);

-- Tip: always list the column names. An INSERT without a column list
-- breaks as soon as someone adds a column to the table.

SELECT * FROM company_db.test_table;
SELECT * FROM company_db.test_table WHERE id > 1;          -- filter rows
SELECT * FROM company_db.test_table ORDER BY name DESC;    -- sort (ASC default)
SELECT * FROM company_db.test_table LIMIT 2;               -- first 2 rows only
SELECT name AS student_name FROM company_db.test_table;    -- AS = alias (rename in output)
SELECT COUNT(*) AS total_rows FROM company_db.test_table;  -- count rows

-- ADD a column. Existing rows get NULL in the new column.
ALTER TABLE company_db.test_table
ADD Email VARCHAR(255);


-- Other common ALTER operations (extra):
-- ALTER TABLE company_db.test_table MODIFY COLUMN email_id VARCHAR(100);  -- change data type
-- ALTER TABLE company_db.test_table DROP COLUMN email_id;                 -- delete a column
-- ALTER TABLE company_db.test_table RENAME TO new_table_name;             -- rename the table

SELECT * FROM company_db.test_table;
-- Syntax: UPDATE table SET column = value WHERE condition;
-- DANGER: without WHERE, EVERY row is updated!
UPDATE company_db.test_table
SET email_id = 'alice@example.com'
WHERE id = 1;

SELECT * FROM company_db.test_table;


/* =====================================================================
   SECTION 8: CONSTRAINTS
   ---------------------------------------------------------------------
   Constraints are RULES that control what data a table accepts.
   They keep data accurate and consistent.
   Types: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT
   ===================================================================== */

-- ---------------------------------------------------------------------
-- 8.1 NOT NULL and UNIQUE
-- ---------------------------------------------------------------------
-- NOT NULL : the column can never be empty (NULL = "no value / unknown").
-- UNIQUE   : no two rows can have the same value in that column.
--            (UNIQUE allows NULL values.)

DROP TABLE IF EXISTS company_db.Persons;

CREATE TABLE company_db.Persons (
    ID        INT NOT NULL UNIQUE,
    LastName  VARCHAR(255) NOT NULL,
    FirstName VARCHAR(255),
    Age       INT
);

INSERT INTO company_db.Persons (ID, LastName, FirstName, Age)
VALUES (1, 'Smith', 'John', 30);

-- NULLs are allowed for FirstName and Age (they have no NOT NULL).
INSERT INTO company_db.Persons (ID, LastName, FirstName, Age)
VALUES (2, 'Doe', NULL, NULL);

-- [WILL FAIL] ID = 1 already exists -> violates UNIQUE
--   Error: "Duplicate entry '1' for key ..."
-- INSERT INTO company_db.Persons (ID, LastName, FirstName, Age)
-- VALUES (1, 'Brown', 'Charlie', 25);

-- [WILL FAIL] LastName is NOT NULL
--   Error: "Column 'LastName' cannot be null"
-- INSERT INTO company_db.Persons (ID, LastName, FirstName, Age)
-- VALUES (3, NULL, 'Alice', 28);

SELECT * FROM company_db.Persons;

-- Note: to test for NULL use IS NULL / IS NOT NULL, never "= NULL".
SELECT * FROM company_db.Persons WHERE FirstName IS NULL;

-- ---------------------------------------------------------------------
-- 8.2 PRIMARY KEY
-- ---------------------------------------------------------------------
-- A PRIMARY KEY uniquely identifies each row.
--   PRIMARY KEY = NOT NULL + UNIQUE
--   A table can have ONLY ONE primary key (it may use several columns:
--   a "composite" key, e.g. PRIMARY KEY (student_id, course_id)).

-- Add a primary key to an existing table
ALTER TABLE company_db.Persons
ADD PRIMARY KEY (ID);

SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'company_db'
  AND TABLE_NAME   = 'Persons';
-- To show only primary keys, add:  AND CONSTRAINT_TYPE = 'PRIMARY KEY'

-- Drop the primary key
ALTER TABLE company_db.Persons
DROP PRIMARY KEY;

-- Add it back using the "named constraint" syntax.
-- NOTE: in MySQL a primary key is ALWAYS named PRIMARY. The name
-- "PK_Person" is accepted (it is standard SQL, used in SQL Server/Oracle)
-- but MySQL ignores it.
ALTER TABLE company_db.Persons
ADD CONSTRAINT PK_Person PRIMARY KEY (ID);

-- Extra: AUTO_INCREMENT makes MySQL generate the id for you:
--   CREATE TABLE demo (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));
--   INSERT INTO demo (name) VALUES ('A'), ('B');   -- ids 1, 2 are created

-- ---------------------------------------------------------------------
-- 8.3 FOREIGN KEY
-- ---------------------------------------------------------------------
-- A FOREIGN KEY is a column (or columns) in one table that refers to the
-- PRIMARY KEY of another table. It links the two tables.
--   Parent (referenced) table : has the primary key  -> Persons
--   Child table               : has the foreign key  -> Orders
--
-- Referential actions (what happens to child rows when the parent changes):
--   RESTRICT / NO ACTION : block the change if child rows exist
--   CASCADE              : apply the same change to child rows
--   SET NULL             : set the child's FK column to NULL
--   SET DEFAULT          : not supported by InnoDB

DROP TABLE IF EXISTS company_db.Orders;

CREATE TABLE company_db.Orders (
    OrderID   INT PRIMARY KEY,
    OrderDate DATE,
    PersonID  INT,
    FOREIGN KEY (PersonID) REFERENCES company_db.Persons(ID)
        ON DELETE RESTRICT     -- can't delete a person who has orders
        ON UPDATE CASCADE      -- if person's ID changes, orders follow
);

-- OK: Person 1 exists in the parent table
INSERT INTO company_db.Orders (OrderID, OrderDate, PersonID)
VALUES (1001, '2024-06-10', 1);

SELECT * FROM company_db.Orders;    -- child
SELECT * FROM company_db.Persons;   -- parent

-- [WILL FAIL] PersonID 999 doesn't exist in Persons
--   Error 1452: "Cannot add or update a child row: a foreign key
--   constraint fails"
-- INSERT INTO company_db.Orders (OrderID, OrderDate, PersonID)
-- VALUES (1002, '2024-06-11', 999);

-- [WILL FAIL] ON DELETE RESTRICT: Person 1 still has an order
--   Error 1451: "Cannot delete or update a parent row..."
-- DELETE FROM company_db.Persons WHERE ID = 1;

-- WORKS thanks to ON UPDATE CASCADE: Persons.ID changes 1 -> 4 and
-- Orders.PersonID is automatically changed from 1 to 4.
UPDATE company_db.Persons SET ID = 4 WHERE ID = 1;

SELECT * FROM company_db.Persons;   -- parent: ID is now 4
SELECT * FROM company_db.Orders;    -- child : PersonID is now 4 too

-- Extra: join the two tables to see them together
SELECT o.OrderID, o.OrderDate, p.FirstName, p.LastName
FROM company_db.Orders o
JOIN company_db.Persons p ON p.ID = o.PersonID;

-- ---------------------------------------------------------------------
-- 8.4 CHECK and DEFAULT
-- ---------------------------------------------------------------------
-- CHECK   : the value must satisfy a condition (enforced in MySQL 8.0.16+;
--           older versions parse it but ignore it).
-- DEFAULT : value used when you don't supply one.

DROP TABLE IF EXISTS company_db.employee;

CREATE TABLE company_db.employee (
    ID        INT NOT NULL,
    LastName  VARCHAR(255) NOT NULL,
    FirstName VARCHAR(255),
    Age       INT CHECK (Age >= 18),
    city      VARCHAR(255) DEFAULT 'new york'
);

-- OK: Age 19 passes the CHECK, city is given explicitly
INSERT INTO company_db.employee (ID, LastName, FirstName, Age, city)
VALUES (1, 'joey', 'tribiani', 19, 'texas');

-- OK: city is not supplied, so the DEFAULT 'new york' is used
INSERT INTO company_db.employee (ID, LastName, FirstName, Age)
VALUES (2, 'jim', 'halpert', 22);

-- [WILL FAIL] Age 15 violates CHECK (Age >= 18)
--   Error 3819: "Check constraint ... is violated"
-- INSERT INTO company_db.employee (ID, LastName, FirstName, Age)
-- VALUES (3, 'kid', 'test', 15);

SELECT * FROM company_db.employee;


/* =====================================================================
   SECTION 9: DELETE vs TRUNCATE vs DROP
   ---------------------------------------------------------------------
   | Feature            | DELETE        | TRUNCATE   | DROP                 |
   |--------------------|---------------|------------|----------------------|
   | Category           | DML           | DDL        | DDL                  |
   | What it removes    | chosen rows   | all rows   | whole table          |
   | WHERE clause       | YES           | NO         | NO                   |
   | Structure kept?    | YES           | YES        | NO (table is gone)   |*/
   
SELECT * FROM company_db.test_table;
SELECT * FROM company_db.test_table WHERE id = 1;

-- MySQL Workbench "Safe Update Mode" blocks UPDATE/DELETE that don't use a
-- key column in WHERE. This turns it off for the current session.
SET SQL_SAFE_UPDATES = 0;

-- DELETE: removes only the rows that match WHERE.
-- WARNING: DELETE without WHERE removes ALL rows (but keeps the table).
DELETE FROM company_db.test_table WHERE id = 1;
SELECT * FROM company_db.test_table;

-- TRUNCATE: removes ALL rows quickly, keeps the table structure.
SELECT * FROM company_db.employee;
TRUNCATE TABLE company_db.employee;
SELECT * FROM company_db.employee;     -- empty, but the table still exists

-- DROP: removes the whole table (structure + data).
DROP TABLE company_db.test_table;
DROP TABLE company_db.employee;
-- SELECT * FROM company_db.test_table;   -- would now give "table doesn't exist"
/* =====================================================================
   SECTION 11: DCL - PERMISSIONS  (extra topic, for reference)
   ---------------------------------------------------------------------
   Needs an admin account (e.g. root). Left commented so it won't change
   your server by accident.
   ===================================================================== */

-- CREATE USER 'student'@'localhost' IDENTIFIED BY 'StrongPassword123!';
-- GRANT SELECT, INSERT ON company_db.* TO 'student'@'localhost';   -- give rights
-- REVOKE INSERT ON company_db.* FROM 'student'@'localhost';        -- take one back
-- SHOW GRANTS FOR 'student'@'localhost';                           -- list rights
-- DROP USER 'student'@'localhost';


DROP TABLE IF EXISTS company_db.Orders;    -- child first
DROP TABLE IF EXISTS company_db.Persons;   -- then parent

DROP DATABASE IF EXISTS company_db;        -- finally the database

-- Re-enable safe update mode (good habit)
SET SQL_SAFE_UPDATES = 1;
