from config import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

conn_string = config.get('database', 'conn_string')
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
db = SQLAlchemy(app)

from app import models
from app import views
