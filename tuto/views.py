from .app import app
from flask import render_template
from .models import get_sample
from flask import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired


class AuthorForm ( FlaskForm ):
    id = HiddenField ('id')
    name = StringField ('Nom', validators =[ DataRequired ()])

@app.route("/edit/author/<int:id >")
def edit_author (id):
    a = get_author(id)
    f = AuthorForm (id=a.id, name=a.name)
    return render_template("edit - author.html", author=a, form=f)


# @app.route("/")
# def home():
#    return "<h1> Hello World </h1>"


# @app.route("/")
# def home():
#     return render_template(
#         "home.html",
#         title="Hello World !",
#         names=["Pierre", "Paul", "Corinne"])

@app.route("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample()
    )

@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template("detail.html", b=book)
