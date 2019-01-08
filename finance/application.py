import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Search user's transaction history from database (history table)
    rows = db.execute(
        "SELECT symbol, sum(shares) sum FROM history WHERE id= :id GROUP BY symbol HAVING sum(shares) > 0", id=session["user_id"])

    # Search user's cash from database (user table)
    result = db.execute("SELECT cash FROM users WHERE id= :id", id=session["user_id"])

    # Store necessary values to send to "index.html" (convert price and cash to USD values)
    count = len(rows)
    grand_total = result[0]["cash"]
    cash = usd(grand_total)
    symbols = []
    shares = []
    prices = []
    totals = []

    # store values, convert prices for each symbol, and add all for grand total value (cash)
    for row in rows:
        quote = lookup(row["symbol"])
        symbols.append(row["symbol"].upper())
        shares.append(row["sum"])
        prices.append(usd(quote["price"]))
        total = row["sum"] * quote["price"]
        totals.append(usd(total))
        grand_total += total

    # convert grand total value to usd values
    grand_total = usd(grand_total)

    return render_template("index.html", count=count, cash=cash, symbols=symbols, shares=shares, prices=prices, totals=totals, grand_total=grand_total)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add additional cash to user's account"""

    # User reached route via POST (by submitting form)
    if request.method == "POST":

        # Ensure cash is submitted
        if not request.form.get("cash"):
            return apology("must sumbit cash", 400)

        # Ensure cash is integer, not fractional
        elif not request.form.get("cash").isdigit():
            return apology("cash must be integer", 400)

        # Ensure cash is positive integer
        elif int(request.form.get("cash")) <= 0:
            return apology("cash must be positive integer", 400)

        # Update cash in database (users table)
        result = db.execute("UPDATE users SET cash = cash + :add WHERE id= :id",
                            add=request.form.get("cash"), id=session["user_id"])

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("addcash.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("symbol does not exist", 400)

        # Ensure number of shares was sumbitted
        elif not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Ensure the input is an integer, not fractional
        elif not request.form.get("shares").isdigit():
            return apology("shares must be integer", 400)

        # Ensure that input is a positive integer
        elif int(request.form.get("shares")) <= 0:
            return apology("shares must be positive integer", 400)

        # Ensure user has enough cash to buy
        rows = db.execute("SELECT cash FROM users WHERE id= :id", id=session["user_id"])
        quote = lookup(request.form.get("symbol"))
        price = quote["price"]
        cost = int(request.form.get("shares")) * price
        cash = rows[0]["cash"]
        if cost > cash:
            return apology("cannot afford the shares", 403)

        # update purchases on database (history table)
        result = db.execute("INSERT INTO history ('id', 'symbol', 'shares', 'price', 'datetime') VALUES (:id, :symbol, :shares, :price, DATETIME('NOW'))",
                            id=session["user_id"], symbol=request.form.get("symbol"), shares=request.form.get("shares"), price=price)
        if not result:
            return apology("cannot insert purchase", 403)

        # update amount of cash on database (users table)
        result = db.execute("UPDATE users SET cash= cash - :cost WHERE id= :id", cost=cost, id=session["user_id"])
        if not result:
            return apology("cannot update cash", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Store necessary information of transaction history from database (history table)
    count = 0
    symbols = []
    shares = []
    prices = []
    datetimes = []
    rows = db.execute("SELECT symbol, shares, price, datetime FROM history WHERE id= :id", id=session["user_id"])
    for row in rows:
        symbols.append(row["symbol"])
        shares.append(row["shares"])
        prices.append(row["price"])
        datetimes.append(row["datetime"])
        count += 1
    return render_template("history.html", count=count, symbols=symbols, shares=shares, prices=prices, datetimes=datetimes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure quote input is valid
        if not request.form.get("symbol"):
            return apology("must submit symbol", 400)

        # Lookup the given symbol (via POST) and store in quote (type dict)
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        # Ensure stock exists
        if not quote:
            return apology("stock does not exists", 400)

        # Direct user towards "quoted.html" while passing quote
        price = usd(quote["price"])
        return render_template("quoted.html", symbol=symbol, price=price)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitter
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password not matching", 400)

        # Insert new user into database
        hashed_password = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hashed_password)

        # Ensure username is unique (not already registered)
        if not result:
            return apology("already registered", 400)

        # If successfully registered, login automatically
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (by submitting a form via POST)
    if request.method == "POST":

        # Ensure select was submitted
        if not request.form.get("symbol"):
            return apology("must submit symbol", 400)

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must submit shares", 400)

        # Ensure number of shares to sell is a positive integer
        elif int(request.form.get("shares")) <= 0:
            return apology("shares must be positive integer", 400)

        # Ensure user has enough shares to sell
        rows = db.execute("SELECT symbol, sum(shares) FROM history WHERE id= :id GROUP BY symbol", id=session["user_id"])
        index = 0
        for i in range(len(rows)):
            if rows[i]["symbol"] == request.form.get("symbol"):
                index = i
        holdings = rows[index]["sum(shares)"]
        if holdings <= 0:
            return apology("don't have any shares", 400)
        elif holdings < int(request.form.get("shares")):
            return apology("don't have enough shares", 400)

        # Update sales on database (history table)
        quote = lookup(request.form.get("symbol"))
        price = quote["price"]
        converted_shares = 0 - int(request.form.get("shares"))
        result = db.execute("INSERT INTO history ('id', 'symbol', 'shares', 'price', 'datetime') VALUES (:id, :symbol, :shares, :price, DATETIME('NOW'))",
                            id=session["user_id"], symbol=request.form.get("symbol"), shares=converted_shares, price=price)
        if not result:
            return apology("cannot insert purchase", 403)

        # Update amount of cash on database (users table)
        sales = int(request.form.get("shares")) * price
        result = db.execute("UPDATE users SET cash= cash + :sales WHERE id= :id", sales=sales, id=session["user_id"])
        if not result:
            return apology("cannot update cash", 403)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        symbols = []
        rows = db.execute("SELECT symbol FROM history WHERE id= :id GROUP BY symbol", id=session["user_id"])
        for row in rows:
            symbols.append(row["symbol"])

        # Display sell page while enabling stock symbols for select
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
