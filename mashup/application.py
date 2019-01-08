import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")


@app.route("/articles")
def articles():
    """Look up articles for geo (when marker is clicked) """

    # Ensure GET request is made
    if request.method != "GET":
        raise RuntimeError("no get request")

    # User reached route via GET (geo has been passed by clicking a marker or the url was typed in)
    else:
        # Lookup geo and retrieve articles
        articles = []
        temp = lookup(request.args.get("geo"))

        # If there are a lot of articles, only store 5
        if len(temp) > 5:
            for i in range(5):
                articles.append(temp[i])
        # Else, store all articles
        else:
            for i in range(len(temp)):
                articles.append(temp[i])
    # return articles in JSON
    return jsonify(articles)


@app.route("/search")
def search():
    """Search for places that match query"""

    # Remove Country Code from query (since using US locations only; erase if allowing other countries)
    query = request.args.get("q").replace("US", " ")

    # Remove unnecessary decorators
    query = query.replace(",", " ").replace("+", " ")

    # Split query into individual words
    query = query.split()

    # If query is single word, just copy it in words list
    words = []
    if len(query) == 1:
        words = query.copy()

    # If query is not single word, check if certain words should be concatenated
    else:

        # Create list and variable for storing concatenating words
        words = []
        concat = query[0]

        # Iterate over all the words
        for q in query[1:]:

            # Check whether the single word or concatenated word has any matches
            result = db.execute(
                "SELECT COUNT(*) FROM places WHERE place_name LIKE :q OR admin_name1 LIKE :q OR admin_code1 LIKE :q OR postal_code LIKE :q", q=concat + " " + q + "%")

            # If there is a match, concatenate the word
            if result[0]["COUNT(*)"] != 0:
                concat += " " + q

            # If adding the next word has no match, add finished concatenation and initialize new concatenation
            else:
                words.append(concat)
                concat = q

        # Add last word to list
        words.append(concat)

    # Create SQL SELECT command string for all of the words (concatenate into one single string)
    command = "SELECT * FROM places WHERE"

    # Append each command string for each words to find overlapping matches
    for i in range(len(words)):

        # Append SQL wildcard % to each word to use LIKE
        words[i] = words[i] + "%"

        # Enable overlapping by using "AND" (for intersection)
        if i != 0:
            command = command + " AND "

        # Append created argument to command string
        command = command + "(place_name LIKE '" + words[i] + "' OR admin_name1 LIKE '" + words[i] + \
            "' OR admin_code1 LIKE '" + words[i] + "' OR postal_code LIKE '" + words[i] + "')"

    # Find overlapping matches of all of the words from the database (places table)
    rows = db.execute(command)

    # Return location data in JSON format
    return jsonify(rows)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
