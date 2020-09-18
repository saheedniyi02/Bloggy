from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Length,Email
from blog.models import User

class PostForm(FlaskForm):
	title=StringField("title",validators=[DataRequired(),Length(min=5,max=50)])
	content=TextAreaField("content",validators=[DataRequired(),Length(min=30,max=2000)])
	submit=SubmitField("post")
	

class CommentFormCurrent(FlaskForm):
    comment=TextAreaField("comment",validators=[DataRequired()])
    submit=SubmitField("Comment")
    
    
class CommentFormAnonymous(FlaskForm):
    email=StringField("email",validators=[Email()])
    comment=TextAreaField("comment",validators=[DataRequired()])
    submit=SubmitField("Comment")
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
        	raise ValidationError("This email has been registered to an account here!! Kindly login to comment")
    