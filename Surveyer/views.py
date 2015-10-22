# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:33:51 2015

@author: Quentin ANDRE
"""

from Surveyer import app, lm, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from .models import User
from .emails import send_password
from .questions import SurveyPage


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(turkid):
    return User.query.get(str.lower(turkid))


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/questions/')
@login_required
def questions():
    return render_template('questions.html', survey_page=SurveyPage(1).questions)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        return render_template("layout.html")
    if request.method == "POST":
        turkid = request.form.get("turkid")
        pw = request.form.get("password")
        u = load_user(turkid)
        if u is not None:
            if u.check_password(pw):
                flash("You have logged in", 'alert-success')
                login_user(u)
                return redirect(url_for('login'))
            else:
                flash("Wrong password. Please double-check or <a href='/forgot_password'>reset your password</a>.",
                      "alert-danger")
                return redirect(url_for('login'))
        else:
            flash("User name not found. Please double-check or <a href='/signin'>sign-in</a> for an account",
                  "alert-warning")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        if g.user is not None and g.user.is_authenticated:
            flash("You are already connected as {}".format(g.user.get_nickname()), "alert-warning")
            return redirect(url_for('login'))
        else:
            return render_template('signin.html')
    elif request.method == 'POST':
        turkid = request.form.get('turkid')
        q = load_user(turkid)
        if q:
            flash("There is already an account associated with this MTurk ID!", "alert-danger")
            return redirect(url_for('signin'))
        else:
            nickname = request.form.get('nickname')
            email = request.form.get('email')
            password = request.form.get('password')
            u = User(turkid, nickname, email, password)
            db.session.add(u)
            db.session.commit()
            flash("Account successfully created!", "alert-success")
            return redirect(url_for('signin'))
    else:
        pass


@app.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        turkid = request.form.get('turkid')
        email = request.form.get('email')
        u = load_user(turkid)
        if u:
            if u.email == email:
                send_password(u, u.get_token())
                flash("Reset instructions have been sent to your email address.", "alert-success")
            else:
                flash("The MTurk Worker ID and the email address do not match.", "alert-danger")
        else:
            flash("User name not found. Please double-check or <a href='/signin'>sign-in</a> for an account",
                  "alert-warning")
    return render_template('forgot_password.html')


@app.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        token = request.args.get('token', None)
        verif = User.verify_token(token)
        if verif:
            session["toggle"] = token
            return render_template('reset_password.html')
        else:
            flash('Invalid token.')
            return redirect(url_for('signin'))
    if request.method == 'POST':
        password = request.form.get('password')
        u = User.verify_token(session["toggle"])
        u.pw_hash = u.hash_password(password)
        flash("Your new password has been recorded.")
        db.session.commit()
        return render_template('layout.html')
