from __main__ import app
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, url_for, redirect
import forms
from flask_bcrypt import Bcrypt
from models import User
from app import bcrypt
from flask_login import LoginManager


##login manager configured here
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#user_id callback in session below 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        email=User.query.filter_by(email=form.email.data).first()
        if email:
            if bcrypt.check_password_hash(email.password, form.password.data):
                login_user(email)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        app.db.session.add(new_user)
        app.db.session.commit()
        print('database added')
        return redirect(url_for('login'))
        
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('home.html')