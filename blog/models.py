from datetime import datetime 
from flask_login import UserMixin
from blog import db,login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	


class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(15),unique=True,nullable=False)
	password=db.Column(db.String(100),nullable=False)
	email=db.Column(db.String(50),unique=True,nullable=False)
	information=db.Column(db.String(100))
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
