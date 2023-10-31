import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, Length

scriptdir = os.path.dirname(os.path.abspath(__file__))
lib_dbfile = os.path.join(scriptdir, "library.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.Unicode, nullable=False)
    last = db.Column(db.Unicode, nullable=False)
    middle = db.Column(db.Unicode, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, first, last, middle=None):
        self.first = first
        self.last = last
        self.middle = middle

    def __str__(self):
        return f"Author(name={self.first}, {self.last})"

    def __repr__(self):
        return str(self)
    
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.Unicode, nullable=False)
    year = db.Column(db.Integer, nullable=True)

    def __init__(self, aid, title, year=None):
        self.aid = aid
        self.title = title
        self.year = year

    def __str__(self):
        return f"Book(title={self.title})"

    def __repr__(self):
        return str(self)

class AuthorForm(FlaskForm):
    first = StringField("first name", validators=[InputRequired()])
    last = StringField("last name", validators=[InputRequired()])
    middle = StringField("middle initial", validators=[Optional(), Length(1,1)])
    submit = SubmitField("submit")

class BookForm(FlaskForm):
    author = SelectField("author", choices=[(0, 'Select an option')], validators=[InputRequired()])
    title = StringField("title", validators=[InputRequired()])
    year = IntegerField("year", validators=[Optional()])
    submit = SubmitField("submit")

with app.app_context():
    db.drop_all()
    db.create_all()
    multiple_instances = [
        Author(first="Jane", last="Austen"),
        Author(first="Louisa", last="Alcott", middle="M"),
        Author(first="Lucy", last="Montgomery", middle="M")
    ]
    db.session.add_all(multiple_instances)
    db.session.commit()
    multiple_instances = [
        Book(aid=1, title="Pride and Prejudice", year=1813),
        Book(aid=1, title="Sense and Sensibility", year=1811),
        Book(aid=2, title="Little Women", year=1868),
        Book(aid=3, title="Anne of Green Gables", year=1908),
        Book(aid=3, title="Emily of New Moon", year=1923)
    ]
    db.session.add_all(multiple_instances)
    db.session.commit()