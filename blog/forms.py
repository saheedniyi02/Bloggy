from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,ValidationError
from wtforms.validators import Length,DataRequired,EqualTo
from blog.models import User


class RegisterForm(FlaskForm):
	username=StringField("username",validators=[Length(min=3,max=15),DataRequired()])
	email=StringField("email",validators=[Length(min=7,max=40),DataRequired()])
	password=PasswordField("password",validators=[Length(min=6,max=15),DataRequired()])
	confirm_password=PasswordField("Confirm Password",validators=[Length(min=6,max=15),DataRequired(),EqualTo("password")])
	submit=SubmitField("Sign up")
	
	
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That username is taken!!! Kindly choose another one")
	
	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username is taken!!! Kindly choose another one")
			
			
class LoginForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired(),Length(min=3,max=15)])
	password=PasswordField("password",validators=[DataRequired(),Length(min=6,max=15)])
	remember=BooleanField("remember me?")
	submit=SubmitField("Sign in")
	


class PostForm(FlaskForm):
	title=StringField("title",validators=[DataRequired(),Length(min=5,max=50)])
	content=TextAreaField("content",validators=[DataRequired(),Length(min=30,max=2000)])
	submit=SubmitField("post")
	

class CommentForm(FlaskForm):
    email=StringField("email",validators=[DataRequired()])
    comment=TextAreaField("comment",validators=[DataRequired()])
    submit=SubmitField("Comment")
    
class UpdateProfile(FlaskForm):
    username=StringField("username",validators=[DataRequired(),Length(min=3,max=15)])
    picture=FileField("Profile Picture",validators=[FileAllowed(["png","jpg"])])
    email=StringField("email",validators=[Length(min=7,max=40),DataRequired()])
    information=TextAreaField("About me")
    twitter=StringField("Twitter username")
    linkedin=StringField("Linkedin username")
    instagram=StringField("Instagram username")
    submit=SubmitField("Update Profile")
    
    def validate_username(self,username):
    	user=User.query.filter_by(username=username.data).first()
    	if user:
    		raise ValidationError("That username has been chosen, Kindly choose another one")
    		
    def validate_email(self,email):
    	user=User.query.filter_by(email=email.data).first()
    	if user:
    		raise ValidationError("That email is taken!! Kindly choose another one")
    	


class RequestResetForm(FlaskForm):
	email=StringField('email',validators=[DataRequired()])
	submit=SubmitField("Rquest Reset password")
	
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()
		
		if not user:
			raise ValidationError("There is no account registered with this email, kindly check your email.")
	
	
class ResetPasswordForm(FlaskForm):
	password=PasswordField("the password",validators=[DataRequired()])
	confirm_password=PasswordField("the confirm password",validators=[DataRequired(),EqualTo("password")])
	submit=SubmitField("Reset password")
	
class SubscribeField(FlaskForm):
	email=StringField("email",validators=[Length(min=7,max=40),DataRequired()])
	submit=SubmitField("Subscribe")
	
							
					