from function14 import sql_search_title, sql_search_year, sql_search_rating, sql_search_listed_in
from flask import Flask


app = Flask(__name__)


@app.route('/movie/<title>')
def page_title(title):
    title_list = sql_search_title(title)
    return title_list


@app.route('/movie/<year1>:<year2>')
def page_year(year1, year2):
    year_list = sql_search_year(year1, year2)
    return year_list


@app.route('/rating/<rating>')
def page_rating(rating):
    rating_list = sql_search_rating(rating)
    return rating_list


@app.route('/genre/<genre>')
def page_genre(genre):
    genre_list = sql_search_listed_in(genre)
    return genre_list


app.run()
