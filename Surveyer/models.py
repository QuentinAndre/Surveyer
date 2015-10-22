# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:14:56 2015

@author: Quentin ANDRE
"""

from Surveyer import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from instance.config import SECRET_KEY


class User(db.Model):
    __tablename__ = 'Users'
    turkid = db.Column(db.String(50), primary_key=True, index=True)
    nickname = db.Column(db.String(50))
    email = db.Column(db.String(60))
    pw_hash = db.Column(db.String(60))
    responses = db.relationship('Answer', backref='user', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __init__(self, turkid, nickname, email, password):
        self.turkid = str.lower(turkid)
        self.nickname = nickname
        self.email = email
        self.pw_hash = self.hash_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.nickname)

    def get_token(self, expiration=1800):
        s = Serializer(SECRET_KEY, expiration)
        return s.dumps({'user': self.turkid}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return None
        turkid = data.get('user')
        if turkid:
            return User.query.get(turkid)
        else:
            return None

    @staticmethod
    def hash_password(password):
        pw_hash = generate_password_hash(password)
        return pw_hash

    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)

    def get_id(self):
        return str(self.turkid)

    def get_nickname(self):
        return str(self.nickname)


class Survey(db.Model):
    __tablename__ = "Surveys"
    surveyid = db.Column(db.String(50), primary_key=True, index=True)
    responses = db.relationship('Answer', backref='survey', lazy='dynamic')

    def __init__(self):
        self._active = False
        self.name = self.surveyid

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if not isinstance(value, 'bool'):
            raise ValueError('Status type not understood, should be Boolean')
        else:
            self._active = value


class Answer(db.Model):
    __tablename__ = "Answers"
    qid = db.Column(db.String(50), primary_key=True, index=True)
    response = db.Column(db.String(50))
    surveyid = db.Column(db.Integer, db.ForeignKey('Surveys.surveyid'))
    turkid = db.Column(db.Integer, db.ForeignKey('Users.turkid'))
