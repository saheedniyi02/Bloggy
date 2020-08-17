from blog.models import User,Post,Comment,Reply
from flask import render_template,url_for,flash,redirect,request,abort
from blog.forms import LoginForm,RegisterForm,PostForm,CommentForm,UpdateProfile,RequestResetForm,ResetPasswordForm
from . import app,db,bcrypt,mail
from flask_login import login_user,logout_user,login_required,current_user
import secrets
from PIL import Image
import os
from flask_mail import Message
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
		if user and bcrypt.check_password_hash(user.password,form.password.data):
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
	image_path=url_for("static",filename="profile_pics/"+user.image)
	
	return render_template("profile.html",user=user,image_path=image_path)


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
		
@app.route("/comment/<int:post_id>",methods=["GET","POST"])
def comment(post_id):
	post=Post.query.get(post_id)
	form=CommentForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			comment=Comment(name=current_user.email[6],email=current_user.email,comment=form.comment.data,topic=post)
		else:
			comment=Comment(name=form.email.data[6],email=form.email.data,comment=form.comment.data,topic=post)
		db.session.add(comment)
		db.session.commit()
	return redirect(url_for("post",id=post_id))	
	return render_template("comment.html",form=form,legend="Comment")
	
	
@app.route("/reply/<int:comment_id>",methods=["GET","POST"])
def reply(comment_id):
	comment=Comment.query.get(comment_id)
	form=CommentForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			reply=Reply(name=current_user.email[6],email=current_user.email,comment=form.comment.data,replied=comment)
		else:
			reply=Reply(name=form.email.data[6],email=form.email.data,comment=form.comment.data,topic=post)
		db.session.add(reply)
		db.session.commit(reply)
		return redirect(url_for("post",id=post_id))	
	return render_template("comment.html",form=form,legend="Reply")
	

def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(app.root_path,"static/profile_pics",picture_fn)
	
	output_size=(125,125)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn
	
	
		
			
					
@app.route("/updateprofile/<int:user_id>/",methods=["GET","POST"])
@login_required
def updateprofile(user_id):
	user=User.query.get(user_id)
	if current_user!=user:
		abort(403)
	form=UpdateProfile()
	if form.validate_on_submit():
		if form.picture.data:
			user.image=save_picture(form.picture.data)
		user.email=form.email.data
		user.username=form.username.data
		user.information=form.information.data
		user.twitter=form.twitter.data
		user.Linkedin=form.linkedin.data
		user.instagram=form.instagram.data
		flash("Your profile has been updated","success")
		db.session.commit()
		return redirect(url_for("profile",username=user.username))
	elif request.method=="GET":
		form.username.data=user.username
		form.email.data=user.email
		form.twitter.data=user.twitter
		form.instagram.data=user.instagram
		form.linkedin.data=user.Linkedin		
	return render_template("update_profile.html",form=form,legend="Update Profile",user=user)

	
	
def send_request_email(user):
	token=user.get_reset_token()
	msg=Message("User Passsord Reset",sender="nooreply@gmail.com",recipients=[user.email])
	msg.body=f'''Password Reset Email
	To reset your password,kindly click the attached link
	{url_for("resetpassword",token=token,_external=True)}
	
	
	Thank you!!
	'''
	mail.send(msg)
	
			
	
@app.route("/requestreset",methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form=RequestResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_request_email(user)
		flash("A link has been sent to your email,Kindly click that link to reset your password")
		return redirect(url_for('login'))
	return render_template("request_reset.html",form=form,legend="Reset Password")

	
	
@app.route("/resetpassword/<token>",methods=["GET","POST"])
def resetpassword(token):
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	user=User.verify_reset_token(token)
	if user is None:
		flash("That is an invalid or expired link","warning")
		return redirect(url_for("request_reset"))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data)
		user.password=hashed_password
		db.session.commit()
		flash("Your password has been changed,you can now login with your new password","success")
		return redirect(url_for("login"))
	return render_template("reset_password.html",form=form,legend="Reset Password")
	
@app.route("/userposts/<string:username>")
def user_post(username):
	user=User.query.filter_by(username=username).first()
	posts=Post.query.filter_by(author=user)
	return render_template("user_posts.html",posts=posts,user=user)