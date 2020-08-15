from datetime import datetime
from flask import Flask,render_template,url_for,flash,redirect,request
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,LoginManager,login_required,login_user,logout_user
from forms import LoginForm,RegisterForm
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
bcypt=Bcrypt(app)
app.config["SECRET_KEY"]="366621166ghgssertt578ooohvcxxerrww2uuuhjooooigfe222567hhnz"
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
	
class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(15),unique=True,nullable=False)
	password=db.Column(db.String(50),nullable=False)
	email=db.Column(db.String(50),unique=True,nullable=False)
	twitter=db.Column(db.String(30))
	Linkedin=db.Column(db.String(50))
	image=db.Column(db.String(100),nullable=False,default="default.jpg")
	instagram=db.Column(db.String(30))
	posts=db.relationship("Post",backref="author",lazy=True)
	
	
	def __repr__(self):
		return (f"{self.username} user")
	
	
	
class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(50),nullable=False)
	content=db.Column(db.Text,nullable=False)
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
	comment=db.relationship("Comment",backref="topic",lazy=True)
	
	
	def __repr__(self):
		return (f"{self.id} date{self.date_posted}")


class Comment(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),nullable=False)
	comment=db.Column(db.Text,nullable=False)
	email=db.Column(db.String(50),nullable=False)
	replies=db.relationship("Reply",backref="replied")
	post_id=db.Column(db.Integer,db.ForeignKey("post.id"))



class Reply(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.Text(50),nullable=False)
	comment=db.Column(db.Text,nullable=False)
	email=db.Column(db.String(50),nullable=False)
	comment_id=db.Column(db.Integer,db.ForeignKey("comment.id"))




@app.route("/")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html")
		
	
@app.route("/login",methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username).first()
		if user and bcrypt.check_hashed_password(user.password,form.password.data):
			login_user(user,form.remember_data)
			next_page=request.args.get("next")
			return redirect(next_page) if next_page else redirect(url_for("home"))
		flash("You have successfully logged in","success")
		else:
			flash("Check your username and password!!")
	return render_template("login.html",form=form)
	
@app.route("/register",methods=["GET","POST"])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.username.data).decode("utf-8")
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("You have successfully registered! You can now login","success")
		return redirect(url_for("login"))
	return render_template("register.html",form=form)

@app.route("/logout"):
def logout():
	logout_user()
	flash("You have been logged out","info")
	return redirect(url_for("home"))


@app.route("/post")
def post():
	return render_template("post.html")
	
@app.route("/profile")
def profile():
	return render_template("profile.html")

if __name__=="__main__":
	app.run(debug=True)
	
