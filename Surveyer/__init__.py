# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bower import Bower
from flask.ext.mail import Mail

# App setup
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# SQL Alchemy setup
db = SQLAlchemy(app)

# Login manager setup
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Javascript package manager setup
Bower(app)

# Mail setup
mail = Mail(app)

# Surveyer
from Surveyer import views, models
