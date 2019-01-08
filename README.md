# CS50 Psets: Web Programming

> Solutions implemented for `CS50x` from 2016 to 2018.

> Problem Sets (Psets): `Pset 6 to Pset 8`.

> For previous Psets: [Solutions for Pset 1 to Pset 5](https://github.com/JiwoonKim/CS50-Pset-General-Programming)


## Pset6: Similarities
> Solved similarities(the more comfortable version) in June, 2018.

> a web app that depicts the costs of transforming one string into another by measuring the edit distance between two strings.

- `helpers.py`: distances function takes two strings as arguments and returns (via a matrix of costs) the edit distance between one and the other.
  > learned how to calculate edit distance between two strings using __dynamic programming__.
  
- `index.html`: an HTML form via which a user can submit
- `matrix.html`: a page generating a visualization of the matrix returned by distances function (each cell contains a cost).
  > learned how to use Jinja2 templating language.
  
_disclaime: application.py, score, error.html, layout.html, log.html, score.html, and style.css was all made by CS50. _
               _Only the function for calculating the edit distance and displaying the matrix of costs and the html form for two strings was implemented by myself (the web application's server (configuration for routes) and various html files were not implemented by myself)._

## Pset7: Finance
> Solved Finance in July, 2018.

- caesar: a program that encrypts messages using Caesar’s cipher.

- vigenère: a program that encrypts messages using Vigenère’s cipher.

- crack: a program that cracks passwords encryped by C's DES-based crypt function (hash function).
    
> learned 
      
## Pset8: Mashup
> Solved Mashup in July, 2018.

