/* Schema for  `items` database */
/* https://www.sqlitetutorial.net/ */

/*
The USING keyword is used in an INNER JOIN or OUTER JOIN (LEFT JOIN, RIGHT JOIN, or FULL JOIN) to specify
the columns that are used to connect the tables. When you use the USING keyword, you only need to specify
the column names that are common to both tables, rather than having to specify the full column names for each table.

For example, suppose you have two tables named table1 and table2, and both tables have a column named id.
If you want to connect these tables using the id column, you could use the following INNER JOIN query:

SELECT * FROM table1
INNER JOIN table2
USING (id);

This query is equivalent to the following INNER JOIN query that uses the ON keyword to specify the columns
that are used to connect the tables:

SELECT * FROM table1
INNER JOIN table2
ON table1.id = table2.id;

Both of these queries will return a table that contains all rows from both table1 and table2 where the id values
are the same. The resulting table will include all columns from both table1 and table2.

In addition to simplifying the syntax of the JOIN clause, using the USING keyword can also make your query more
readable and easier to understand. It also ensures that the columns used to connect the tables are the same in both tables,
which can help prevent errors in your query.

In SQLite, it is not possible to define a column with a "list" data type. SQLite supports a limited set of data types, including INTEGER, REAL, TEXT, and BLOB, but it does not have a built-in data type for storing lists of values.

If you need to store a list of values in a SQLite table, one option is to use a TEXT field and encode the list as a string
using a delimiter character to separate the values. For example, you could encode a list of integers
as a string like this: "1,2,3,4,5". Then you can use the split() function and a regular expression to split the string
back into a list of values when you want to access the data.

Yes, it is possible to join tables from different databases in SQLite.
To do this, you would first need to create a new database that contains both tables, and then you can use a JOIN clause
in a SELECT statement to combine the data from the two tables. For example:

ATTACH DATABASE 'database1.db' AS db1;
ATTACH DATABASE 'database2.db' AS db2;

SELECT *
FROM db1.table1
JOIN db2.table2
ON db1.table1.column1 = db2.table2.column1;

This query would attach the databases database1.db and database2.db as db1 and db2, respectively,
and then use a JOIN clause to combine data from the table1 and table2 tables based on a common column1 in each table.
*/

-- https://minecraft.fandom.com/wiki/Minecraft_Dungeons:Item

BEGIN TRANSACTION;


CREATE TABLE IF NOT EXISTS melee (
    id                  INTEGER         PRIMARY KEY AUTOINCREMENT,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "common, rare", -- Split string later in Python
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);

CREATE TABLE IF NOT EXISTS ranged (
    id                  INTEGER         PRIMARY KEY AUTOINCREMENT,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "common, rare", -- Split string later in Python
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);

CREATE TABLE IF NOT EXISTS melee_specials (
    is_from             INTEGER         NOT NULL,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "unique",
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);

CREATE TABLE IF NOT EXISTS ranged_specials (
    is_from             INTEGER         NOT NULL,
    name                TEXT            NOT NULL,
    rarity              TEXT            NOT NULL DEFAULT "unique",
    description         TEXT            NOT NULL,
    image_path          TEXT            NOT NULL,
    emoji_string        TEXT            NOT NULL,
    emoji_id            INTEGER         NOT NULL
);

/* INSERT INTO melee (name, description, image_path, emoji_string, emoji_id)
VALUES  (),
        (); */



COMMIT TRANSACTION;