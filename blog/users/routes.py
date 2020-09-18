from flask import Blueprint,abort,request,flash,redirect,render_template,url_for
from flask_login import login_required,current_user,login_user,logout_user
from blog import db,bcrypt
from blog.models import User,Post
from blog.users.forms import LoginForm,RegisterForm,UpdateProfile,RequestResetForm,ResetPasswordForm
from blog.users.utils import save_picture,send_request_email

users=Blueprint('users',__name__)

@users.route("/login",methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,form.remember.data)
			flash("You have been logged in","success")
			next_page=request.args.get("next")
			return redirect(next_page) if next_page else redirect(url_for("main.home"))
		else:
			flash("check email and password","danger")
	return render_template("login.html",form=form,title="login")

	
@users.route("/register",methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form=RegisterForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash("You have successfully registered! You can now login","success")
		return redirect(url_for("users.login"))
	return render_template("register.html",form=form)

@users.route("/profile/<string:username>")
def profile(username):
	user=User.query.filter_by(username=username).first()
	image_path=url_for("static",filename="profile_pics/"+user.image)
	return render_template("profile.html",user=user,image_path=image_path)


@users.route("/logout")
def logout():
	logout_user()
	flash("You have been logged out","info")
	return redirect(url_for("main.home"))

	
		
			
					
@users.route("/updateprofile/<int:user_id>/",methods=["GET","POST"])
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
		return redirect(url_for("users.profile",username=user.username))
	elif request.method=="GET":
		form.username.data=user.username
		form.email.data=user.email
		form.twitter.data=user.twitter
		form.instagram.data=user.instagram
		form.linkedin.data=user.Linkedin		
	return render_template("update_profile.html",form=form,legend="Update Profile",user=user)

	
	

	
			
	
@users.route("/requestreset",methods=["GET","POST"])
def request_reset():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	form=RequestResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_request_email(user)
		flash("A link has been sent to your email,Kindly click that link to reset your password")
		return redirect(url_for('users login'))
	return render_template("request_reset.html",form=form,legend="Reset Password")

	
	
@users.route("/resetpassword/<token>",methods=["GET","POST"])
def resetpassword(token):
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))
	user=User.verify_reset_token(token)
	if user is None:
		flash("That is an invalid or expired link","warning")
		return redirect(url_for("users.request_reset"))
	form=ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data)
		user.password=hashed_password
		db.session.commit()
		flash("Your password has been changed,you can now login with your new password","success")
		return redirect(url_for("users.login"))
	return render_template("reset_password.html",form=form,legend="Reset Password")
	
@users.route("/userposts/<string:username>")
def user_post(username):
	page=request.args.get("page",1,type=int)
	user=User.query.filter_by(username=username).first()
	posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=6,page=page)
	return render_template("user_posts.html",posts=posts,user=user)
	