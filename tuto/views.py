from .app import app, db
from .models import get_sample, get_author, User, get_book, update_author, del_author, del_book

from flask import render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, login_required

from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    next = HiddenField() # la page sur laquelle on arrive
    
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators=[DataRequired()])
  
class DelAuthorForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    
class DelBookForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    
@app.route ("/")
def home():
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample())
    
    
@app.route("/detail/<id>")
def detail(id):
    book = get_book(id)
    return render_template(
    "detail.html",
    book=book)

@app.route("/authors/<id>")
def detail_author(id):
    author = get_author(id)
    return render_template("author.html", author=author)

@app.route("/add/author", methods =("POST", "GET"))
@app.route("/edit-author/<int:id>", methods =("POST", "GET"))
@login_required
def save_author(id: int|None=None):
    a = get_author(id)
    if a :
        f = AuthorForm(id=a.id, name=a.name)
    else:
        f =AuthorForm()

    if f.id.data:
        author_id = int(f.id.data)
    else:
        author_id = None
    a = update_author(author_id, f.name.data)

    if f.validate_on_submit():
        return redirect(url_for('detail_author', id=a.id))
    return render_template(
        "edit-author.html",
        author=a, form=f)

@app.route("/delete/author/", methods =("POST", "GET"))
@login_required
def delete_author(name:str|None=None):
    if name == None :
        f = DelAuthorForm()
    else :
        f = DelAuthorForm(name)
    if f.name.data != None:
        print("view :"+f.name.data)
        del_author(f.name.data)   
        if f.validate_on_submit():
            return redirect(url_for('home')) 

    if f.validate_on_submit():
        return redirect(url_for('home'))
    return render_template(
        "del-author.html",
        form=f)

@app.route("/delete/books/", methods =("POST", "GET"))
@login_required
def delete_books(id:int|None=None):
    if id == None:
        f = DelBookForm()
    else :
        f = DelBookForm(id)
    if f.id.data != None:
        print("view :"+f.id.data)
        del_book(f.id.data)   
        if f.validate_on_submit():
            return redirect(url_for('home')) 

    if f.validate_on_submit():
        return redirect(url_for('home'))
    return render_template(
        "del-book.html",
        form=f)
        
@app.route("/login/",methods=("GET", "POST"))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")

    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(f.next.data if f.next.data != "" else url_for("home"))
    return render_template(
        "login.html",
        form=f)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))
