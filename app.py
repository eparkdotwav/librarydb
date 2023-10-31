import os, sys
from flask import Flask, session, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from database import db, Author, Book, AuthorForm, BookForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xoxoxo'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "library.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
     return redirect(url_for('library'))

@app.route('/library/')
def library():
    books_and_authors = db.session.query(Book, Author).join(Author, Author.id == Book.aid).all()
    return render_template('library.html', books_and_authors=books_and_authors)

@app.route('/authors/', methods=('GET', 'POST'))
def author_form():
    form = AuthorForm()
    if request.method == "GET":
        return render_template("addauthor.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            author = Author(form.first.data, form.last.data, form.middle.data)
            db.session.add(author)
            db.session.commit()
            return redirect(url_for('book_form'))
        else:
            print("flash")
            for field, msg in form.errors.items():
                flash(f"{field}: {msg}")
            return render_template("addauthor.html", form=form)
    return redirect(url_for('author_form'))

@app.route('/books/', methods=('GET', 'POST'))
def book_form():
    form = BookForm()

    authors = Author.query.all()
    unique_author_ids = set()
    author_choices = []

    for author in authors:
        if author.id not in unique_author_ids:
            unique_author_ids.add(author.id)
            author_choices.append((author.id, f"author {author.id}: {author.first} {author.last}"))

    form.author.choices = [('', 'Select an author')] + author_choices

    if request.method == "GET":
        return render_template("addbook.html", form=form, author=0)
    if request.method == "POST":
        if form.validate_on_submit():
            book = Book(aid=form.author.data, title=form.title.data, year=form.year.data)
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print("flash")
            for field, msg in form.errors.items():
                flash(f"{field}: {msg}")
                print(msg)
            return redirect(url_for('book_form'))
    return redirect(url_for('index'))