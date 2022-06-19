#Attempting to build a robust login featured enabled web app with replit accomplished functionalities.
#Required modules imported below
#Attempt to comment as best as possible
#Attempt to write cleanest code till date
#Attempt to refactor and organise best code till date 
#KISS - Keep It Simple, Smart ! 

from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

##flask app initialised 

app = Flask(__name__)

##sql database config setting below 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

##bcrpt hashing function initialised for interaction with app below

bcrypt = Bcrypt(app)

##login manager configured here

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


#user_id callback in session below 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##database objects below

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(200), nullable = False)
    email=db.Column(db.String(101), nullable = False, unique = True)
    password=db.Column(db.String(80), nullable = False)

##form objects below

#registration form created below, connected to html

class RegistrationForm(FlaskForm):
    name=StringField(validators=[InputRequired(), Length(min=3, max=120)], render_kw= { "placeholder": "name"})
    email=EmailField(validators=[InputRequired(), Length(min=4, max=20)], render_kw = { "placeholder": "email" } )
    password=PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "password"})
    submit=SubmitField("Register")

    def validate_email(self, email):
        existing_email=User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("Already Exists")

#login form created below, connected to html

class LoginForm(FlaskForm):
    email=EmailField(validators=[InputRequired(), Length(min=4, max=20)], render_kw = { "placeholder": "email" } )
    password=PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "password"})
    submit=SubmitField("Submit")

## views setup below

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=User.query.filter_by(email=form.email.data).first()
        if email:
            if bcrypt.check_password_hash(email.password, form.password.data):
                login_user(email)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
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

## main app initialisation below 

if __name__ == '__main__':
    app.run(debug=True, port=8000)