from datetime import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
app.config["SECRET_KEY"]="36662116thi7o4sacczdw337uj2567hhnz"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'
login_manager=LoginManager(app)
login_manager.login_view="login"



from blog import routes