from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import Length,DataRequired,EqualTo
from app import User


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
	content=TextAreaField("content",validators=[DataRequired()])
	submit=SubmitField("post")
	

class CommentForm(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired()])
    comment=TextAreaField("comment",validators=[DataRequired()])
    submit=SubmitField("Comment")
    
class UpdateProfile(FlaskForm):
    username=StringField("username",validators=[DataRequired(),Length(min=3,max=15)])
    picture=FileField("update profile picture",validators=[FileAllowed(["png","jpg"])])
    email=StringField("email",validators=[Length(min=7,max=40),DataRequired()])
    twitter=StringField("Twitter username")
    linkedin=StringField("Linkedin")
    instagram=StringField("Instagram username")
    submit=SubmitField("Update Profile")


class RequestResetForm(FlaskForm):
	email=StringField('email',validators=[DataRequired()])
	submit=SubmitField("Rquest Reset password")
	
	
class ResetPasswordForm(FlaskForm):
	password=PasswordField("the password",validators=[DataRequired()])
	confirm_password=PasswordField("the confirm password",validators=[DataRequired(),EqualTo("password")])
	submit=SubmitField("Reset password")
	
class SubscribeField(FlaskForm):
	email=StringField("email",validators=[Length(min=7,max=40),DataRequired()])
	submit=SubmitField("Subscribe")
	
							
					