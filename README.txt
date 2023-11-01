code written by: epark
github link: https://github.com/eparkdotwav
made in october 2023

this project is a simple library database. i used python and flask to set up
the server logic, sqlite and sqlalchemy to set up the database, and wtforms to
dynamically receive input from the user before storing it in the database. the
display is created with html and jinja.

upon starting up the server, a user can choose to run different flask routes, leading them
to either an index of all books (and their authors) or a form to add a book or an author.
the index route will display a table of all the books and their authors via html and jinja.
the books route will display a form that asks a user for information needed to add a new
book to the database. the authors route will display a form that asks a user for information
needed to add a new author to the database. more python-flask logic connects the three different
pages together.