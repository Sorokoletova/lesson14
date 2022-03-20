import json
import sqlite3


def sql_all(sql):
    """ возвращает данные из базы по запросу SQL"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        query = connection.execute(sql).fetchall()
        return query


def sql_search_title(title):
    """ возвращает данные из базы по названию(title)"""
    result = sql_all(f"""
                       SELECT title, country, release_year, listed_in, description
                       FROM netflix
                       WHERE  title = '{title}'
                       ORDER BY release_year DESC
                       LIMIT 1
        """)
    for q in result:
        search_title = dict(q)
    return json.dumps(search_title, indent=4)


def sql_search_year(year1, year2):
    """ возвращает данные из базы по годам(year)"""
    result = sql_all(f"""
                           SELECT title, release_year
                           FROM netflix
                           WHERE  release_year BETWEEN '{year1}'AND'{year2}'
                           LIMIT 100
            """)
    result_year = []
    for q in result:
        result_year.append(dict(q))
    return json.dumps(result_year, indent=4)


def sql_search_rating(rating):
    """ возвращает данные из базы по рейтингу (rating)"""
    if rating.lower() == 'children':
        result = sql_all(f"""
                               SELECT title, rating, description 
                               FROM netflix
                               WHERE rating = 'G'
                               
                """)
    elif rating.lower() == 'family':
        result = sql_all(f"""
                                       SELECT title, rating, description 
                                       FROM netflix
                                       WHERE rating = 'G' OR rating = 'PG' OR rating = 'PG-13'

                        """)
    elif rating.lower() == 'adult':
        result = sql_all(f"""
                                               SELECT title, rating, description 
                                               FROM netflix
                                               WHERE rating ='R' OR rating = 'NC-17'

                                """)
    result_rating = []
    for q in result:
        result_rating.append(dict(q))
    return json.dumps(result_rating, indent=4)


def sql_search_listed_in(genre):
    """ возвращает данные из базы по жанру (genre)"""
    result = sql_all(f"""
                                   SELECT title, description 
                                   FROM netflix
                                   WHERE listed_in LIKE '%{genre}%'
                                   ORDER BY release_year DESC
                                   LIMIT 10
                    """)
    result_listed = []
    for q in result:
        result_listed.append(dict(q))
    return json.dumps(result_listed, indent=4)


def sql_search_cast(cast1, cast2):
    """ возвращает данные из базы по актеру (cast)"""
    result = sql_all(f"""
                        SELECT netflix.cast
                        FROM netflix
                        WHERE netflix.cast LIKE '%{cast1}%' AND netflix.cast LIKE '%{cast2}%'  
                        """)
    result_cast = []
    result_name = []
    for q in result:
        a = dict(q).get('cast').split(", ")
        for name in a:
            result_name.append(name)
    two_name = [cast1, cast2]
    names = set(result_name) - set(two_name)
    for name in names:
        n = result_name.count(name)
        if n > 2:
            result_cast.append(name)
    return result_cast


print(sql_search_cast('Rose McIver', 'Ben Lamb'))


def sql_search_all(types, release_year, listed_in):
    """ возвращает данные из базы по типу, году выхода и жанру"""
    result = sql_all(f"""
                                       SELECT *
                                       FROM netflix
                                       WHERE listed_in LIKE '%{listed_in}%'
                                       AND release_year ='{release_year}'
                                       AND type ='{types}'
                                       
                        """)
    result_all = []
    for q in result:
        result_all.append(dict(q))
    return json.dumps(result_all, indent=4)
