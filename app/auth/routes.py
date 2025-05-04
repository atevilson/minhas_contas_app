from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/auth/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.username.data).first():
            flash('Usuário já está cadastrado.', 'warning')
            return render_template('auth/register.html', form=form)

        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        
        login_user(user)
        return redirect(url_for('expenses.dashboard'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/auth/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('expenses.dashboard'))
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))