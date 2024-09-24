# 5f992707-7166-4249-a52c-954cabaef963

from flask import Flask
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap5(app)

import os.path
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),p))

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../myaapp.db'))
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "5f992707-7166-4249-a52c-954cabaef963"