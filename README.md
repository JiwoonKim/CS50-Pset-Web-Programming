# CS50 Psets: Web Programming

> Solutions implemented for `CS50x` from 2016 to 2018.

> Problem Sets (Psets): `Pset 6 to Pset 8`.

> For previous Psets: [Solutions for Pset 1 to Pset 5](https://github.com/JiwoonKim/CS50-Pset-General-Programming)


## Pset6: Similarities
> Solved similarities(the more comfortable version) in June, 2018.

> A web application that depicts the costs of transforming one string into another by measuring the edit distance between two strings.

<img width="400" alt="sim1" src="https://user-images.githubusercontent.com/29671309/50814313-90df8f00-135c-11e9-9bdb-57f244a42077.PNG">  <img width="405" alt="sim2" src="https://user-images.githubusercontent.com/29671309/50814319-96d57000-135c-11e9-8cc7-2bcc2ab55332.PNG">

> _web app: prompts user for two strings and then, displays matrix and log of edit distance between two strings._

- `helpers.py`: function distances takes two strings as arguments and returns (via a matrix of costs) the edit distance between one and the other.
  > learned how to calculate edit distance between two strings using __dynamic programming__.
  
- `index.html`: an HTML form via which a user can submit
- `matrix.html`: a page generating a visualization of the matrix returned by distances function (each cell contains a cost).
  > learned how to create a html form and use Jinja2 templating language.
  
_Only the function for calculating the edit distance and displaying the matrix of costs and the html form for two strings was implemented by myself (the web application's server (configuration for routes using flask framework) and various html files were not implemented by myself)._

## Pset7: Finance
> Solved Finance in July, 2018.

> A web app managing portfolios of stocks. Allows user to check real stocks' actual prices and portfolios' values, and let user simulate purchases and sales of stocks by querying IEX for stocks' prices. 

- `application.py`: a program which serves the web appliction. A server using a flask framework, defines the following methods for routes.
  - `register`: allows user to register for an account by receiving a POST request and inserting the new user into the SQLite3 database.
  - `index`: 
  - `quote`: allows user to look up a stock's current price by receiving 
  - `buy`:
  - `sell`:
  -`history`:
  -`add_cash`: a personal touch to the web appliction to enable the user to add more cash.
  
> learned 

- `register.html`: an HTML for user to submit a form of input fields for id, password, and confirmation to register route.
- `index.html`: 
- `quote.html`:
- `quoted.html`:
- `buy.html`:
- `sell.html`:
- `history.html`:
- `addcash.html`:
  
> learned
      
## Pset8: Mashup
> Solved Mashup in July, 2018.

