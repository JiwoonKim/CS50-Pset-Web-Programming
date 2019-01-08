# CS50 Psets: Web Programming

> Solutions implemented for `CS50x` from 2016 to 2018.

> Problem Sets (Psets): `Pset 6 to Pset 8`.

> For previous Psets: [Solutions for Pset 1 to Pset 5](https://github.com/JiwoonKim/CS50-Pset-General-Programming)


## Pset6: Similarities
> Solved similarities(the more comfortable version) in June, 2018.

> A web application that depicts the costs of transforming one string into another by measuring the edit distance between two strings.

<img width="400" alt="sim1" src="https://user-images.githubusercontent.com/29671309/50814313-90df8f00-135c-11e9-9bdb-57f244a42077.PNG">  <img width="405" alt="sim2" src="https://user-images.githubusercontent.com/29671309/50814319-96d57000-135c-11e9-8cc7-2bcc2ab55332.PNG">

> _prompts user for two strings and then, displays matrix and log of edit distance between two strings._

- `helpers.py`: function distances takes two strings as arguments and returns (via a matrix of costs) the edit distance between one and the other.
  > learned how to calculate edit distance between two strings using __dynamic programming__.
  
- `index.html`: an HTML form via which a user can submit
- `matrix.html`: a page generating a visualization of the matrix returned by distances function (each cell contains a cost).
  > learned how to create a html form and use Jinja2 templating language.
  
  _disclaimer: only the function for calculating the edit distance and displaying the matrix of costs and the html form for two strings was implemented by myself (the web application's server (configuration for routes using flask framework) and various html files were not implemented by myself)._

### What I learned from Pset6
> basic concepts of HTML, CSS, and a web server.

## Pset7: Finance
> Solved Finance in July, 2018.

> A web app managing portfolios of stocks. Allows user to check real stocks' actual prices and portfolios' values, and let user simulate purchases and sales of stocks by querying IEX for stocks' prices. 

- `application.py`: a program which serves the web appliction. A server using a flask framework, defines the following methods for routes.
  - `register`: enables user to register for an account by receiving a POST request from register.html and inserting the new user into the SQLite3 database.
  - `index`: displays a table summarizing the user's portfolio of which stocks the user owns and the user's current cash balance.
  - `quote`: enables user to look up a stock's current price by receiving both GET and POST requests. (GET request for displaying quote.html where user can input a stock's symbol and send a HTML form via POST request which then, renders quoted.html which displays the stock's current price.)
  - `buy`: enables user to simulate a purchase of stocks by receiving a POST request from buy.html and recording the purchase in the database.
  - `sell`: enables user to simulate a sale of stocks by receiving a POST request from buy.html and recording the sale in the database.
  - `history`: displays a table summarizing all of the user's transactions made.
  - `add_cash`: a personal touch to the web appliction to enable the user to add more cash.
  
> learned 

- HTML files
  - `register.html`: an HTML form to prompt user to submit a form for registration (inputs of id, password, and confirmation).
  - `index.html`: an HTML to display a table summarizing the user's portfolio of which stocks the user owns and the user's current balance account.
  - `quote.html`: an HTML form to prompt user for a stock's symbol to look up the current price of a stock.
  - `quoted.html`: an HTML to display the stock's current price.
  - `buy.html`: an HTML form to prompt user to virtually buy stocks.
  - `sell.html`:an HTML form to prompt user to virtually sell stocks.
  - `history.html`: an HTML to display a table summarizing all of the user's transactions made.
  - `addcash.html`: an HTML form to add more cash to the user's balance account.
  
> learned HTML syntax, jinja2 templating language, how to create an HTML form.

  _disclaimer: only the function for calculating the edit distance and displaying the matrix of costs and the html form for two strings was implemented by myself (the web application's server (configuration for routes using flask framework) and various html files were not implemented by myself)._

### What I learned from Pset7
> how a web application is structured using HTML, CSS, and a web server (Flask).

> the MVC (Model-View-Controller) paradigm. Particularly the model and controller.

> how a web server framework (i.e. Flask) handles requests and sends responses.

> how to manipulate data and databases using SQL (Structured Query Language).
      
## Pset8: Mashup
> Solved Mashup in July, 2018.

> 

### What I learned from Pset7
> how a web appl
