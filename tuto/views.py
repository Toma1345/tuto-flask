from .app import app
from flask import render_template
from .models import get_sample

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