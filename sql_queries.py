"""
SQL queries for Sakila database.
Contains all raw SQL queries used by the DB client
for filtering, searching, and retrieving movie data.
"""

GET_CATEGORIES = """
SELECT category_id, name
FROM category
ORDER BY name
"""


GET_YEAR_RANGE = """
SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
FROM film
"""

SEARCH_BY_YEAR = """
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors, 
       lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE f.release_year BETWEEN %s AND %s
GROUP BY f.film_id, f.title, f.release_year, lang.name, f.description
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""


SEARCH_BY_CATEGORY_AND_YEAR = """
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors,
    f.length, lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE c.category_id = %s AND f.release_year BETWEEN %s AND %s
GROUP BY f.film_id, f.title, f.release_year, f.length, lang.name, f.description
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""

SEARCH_FILMS_BY_KEYWORD = """
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors,
    f.length, lang.name AS language_name, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN language AS lang ON f.language_id = lang.language_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE f.title LIKE %s
GROUP BY f.film_id, f.title, f.release_year, f.length, lang.name, f.description
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""

SEARCH_BY_CATEGORY = """
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS categories,
    GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors,
    f.length, lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
WHERE c.category_id = %s
GROUP BY f.film_id, f.title, f.release_year, f.length, lang.name, f.description
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""

COUNT_FILMS_BY_KEYWORD = """
SELECT COUNT(DISTINCT f.film_id) AS count
FROM film AS f
WHERE f.title LIKE %s
"""

COUNT_FILMS_BY_CATEGORY = """
SELECT COUNT(*) AS count
FROM film_category
WHERE category_id = %s
"""

COUNT_FILMS_BY_YEAR = """
SELECT COUNT(*) AS count
FROM film
WHERE release_year BETWEEN %s AND %s
"""

COUNT_FILMS_BY_CATEGORY_AND_YEAR = """
SELECT COUNT(*) AS count
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
WHERE fc.category_id = %s
AND f.release_year BETWEEN %s AND %s
"""

