from blog.models import User,Post,Comment,Reply
from flask import render_template,url_for,flash,redirect,request,abort
from blog.forms import LoginForm,RegisterForm,PostForm,CommentForm
from . import app,db,bcrypt
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime

@app.route("/")
def home():
	posts=Post.query.all()
	return render_template("home.html",posts=posts)

@app.route("/about")
def about():
	return render_template("about.html")
		
	
@app.route("/login",methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash:
			login_user(user,form.remember.data)
			next_page=request.args.get("next")
			return redirect(next_page) if next_page else redirect(url_for("home"))
		else:
			flash("check email and password","danger")
	return render_template("login.html",form=form,title="login")

	
@app.route("/register",methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form=RegisterForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("You have successfully registered! You can now login","success")
		return redirect(url_for("login"))
	return render_template("register.html",form=form)

@app.route("/profile/<string:username>")
def profile(username):
	user=User.query.filter_by(username=username).first()
	return render_template("profile.html",user=user)


@app.route("/logout")
def logout():
	logout_user()
	flash("You have been logged out","info")
	return redirect(url_for("home"))

@app.route("/newpost",methods=["GET","POST"])
@login_required
def create_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data,content=form.content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("Your post has been created","success")
		return redirect("home.html")
	return render_template("create_post.html",form=form,legend="Create Post")


@app.route("/post/update/<int:id>",methods=["POST","GET"])
def update_post(id):
	post=Post.query.get_or_404(id)
	if post.author!=current_user:
		abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash("Your post has been updated!","success")
		return redirect(url_for('post',id=post.id))
	elif request.method=="GET":
		form.title.data=post.title
		form.content.data=post.content
	return render_template("create_post.html",form=form,legend="Update Post")
	
	


@app.route("/post/<int:id>")
def post(id):
	form=CommentForm()
	post=Post.query.get_or_404(id)
	return render_template("post.html",post=post)


@app.route("/post/delete/<int:id>",methods=["POST","GET"])
@login_required
def delete_post(id):
		post=Post.query.get_or_404(id)
		if post.author!=current_user:
			abort(403)
		db.session.delete(post)
		db.session.commit()
		return redirect(url_for("home"))
		
@app.route("/comment")
def comment():
	form=CommentForm()
	return render_template("comment.html",form=form,legend="Comment")