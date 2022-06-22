#Required modules imported per module forms, models, views 
#Attempt to comment as best as possible
#Attempt to write cleanest code till date

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# import session on demand

##flask app initialised 
app = Flask(__name__)

##sql database config setting below 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

##bcrpt hashing function initialised for interaction with app below
bcrypt = Bcrypt(app)

# NOTE: views setup here not after model and form imports
import views
#database model objects below
import models
#form model objects below
import forms

## main app initialisation below 
if __name__ == '__main__':
    app.run(debug=True, port=8000)