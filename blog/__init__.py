from datetime import datetime
from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
login_manager.login_message_category="info"
app.config["SECRET_KEY"]="arandomsecrertkeywouldbegetee"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True

app.config["MAIL_USERNAME"]="saheedflaskappmail@gmail.com"
app.config["MAIL_PASSWORD"]="passwordhere"



mail=Mail(app)

from blog import routes