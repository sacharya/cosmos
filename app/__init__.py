from config import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

conn_string = config.get('db_conn_string')
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
db = SQLAlchemy(app)

from app.db import models
from app.db import dbapi
from app import views
