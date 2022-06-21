from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError


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