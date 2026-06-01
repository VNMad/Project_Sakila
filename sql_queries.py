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
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(c.name SEPARATOR ', ') AS categories, lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
WHERE f.release_year BETWEEN %s AND %s
GROUP BY f.film_id, f.title, f.release_year, lang.name, f.description
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""


SEARCH_BY_CATEGORY_AND_YEAR = """
SELECT f.film_id, f.title, f.release_year, c.name AS categories, f.length, lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
WHERE c.category_id = %s AND f.release_year BETWEEN %s AND %s
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""

SEARCH_FILMS_BY_KEYWORD = """
SELECT f.film_id, f.title, f.release_year, GROUP_CONCAT(c.name SEPARATOR ', ') AS categories, f.length, lang.name AS language_name, f.description
FROM film AS f
LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
LEFT JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN language AS lang ON f.language_id = lang.language_id
WHERE f.title LIKE %s
GROUP BY f.film_id
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""

SEARCH_BY_CATEGORY = """
SELECT f.film_id, f.title, f.release_year, c.name AS categories, f.length, lang.name AS language_name, f.description
FROM film AS f
JOIN film_category AS fc ON f.film_id = fc.film_id
JOIN category AS c ON fc.category_id = c.category_id
JOIN language AS lang ON f.language_id = lang.language_id
WHERE c.category_id = %s
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""