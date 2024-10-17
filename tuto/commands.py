import click
import yaml
from .app import app, db
from .models import Author, Book, User
from hashlib import sha256

@app.cli.command("load_db")
@click.argument('filename')

def loaddb(filename):
    db.create_all()
    
    with open(filename) as file:
        books = yaml.load(file, Loader=yaml.Loader)
    
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()
    
    
    for b in books:
        a = authors[b["author"]]
        o = Book(price = b["price"],
                title = b["title"],
                url = b["url"] ,
                image = b["img"] ,
                author_id = a.id)
        db.session.add(o)
    db.session.commit()
    
@app.cli.command("sync_db")
def syncdb():
    '''
        Create all missing tables
    '''
    db.create_all()
    
@app.cli.command("new_user")
@click.argument('username')
@click.argument('password')
def newuser(username, password):
    """New user"""
   
    m = sha256()
    m.update(password.encode())
    u = User(username=username, password=m.hexdigest())
    db.session.add(u)
    db.session.commit()
    