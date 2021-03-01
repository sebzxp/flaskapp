from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = 'b83887e39f9645a578b9697b9fd62cd8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1427911:14Djent95**@csmysql.cs.cf.ac.uk:3306/c1427911_database1'



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes