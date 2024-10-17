from .app import db
from flask_login import UserMixin
from .app import login_manager

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    
    def get_id(self):
        return self.username
    
class Author(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))

    books = db.relationship("Book", back_populates="author")
    
    def __repr__ (self ):
        return "<Author (%d) %s>" % (self.id , self.name)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Float)
    url = db.Column(db.String(200))
    image = db.Column(db.String(200))
    title = db.Column(db.String(100))

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books")

    def __repr__ (self ):
        return "<Book (%d) %s>" % (self.id , self.title)
    

def get_sample():
    return Book.query.limit(24).all() 

def get_author(id):
    return Author.query.get(id)

def update_author(id, name):
    author = Author.query.get(id)

    if author:
        author.name = name
    else:
        author = Author(id = id, name = name)
        db.session.add(author)
    db.session.commit()
    return author

def del_author(nom):
    author = db.session.query(Author).filter_by(name=nom).first()
    if author:
        db.session.delete(author)
        db.session.commit()

def get_book(id):
    return Book.query.get(id)

def del_book(ident):
    book = db.session.query(Book).filter_by(id=ident).first()
    print(book)
    if book:
        print("suppr")
        db.session.delete(book)
        db.session.commit()