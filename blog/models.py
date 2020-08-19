from datetime import datetime 
from flask_login import UserMixin
from blog import db,login_manager,app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



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
	
	
	def get_reset_token(self,expires_sec=3600):
		s=Serializer(app.config["SECRET_KEY"],expires_sec)
		return s.dumps({"user_id":self.id}).decode("utf-8")
		
		
		
	@staticmethod
	def verify_reset_token(token):
		s=Serializer(app.config["SECRET_KEY"])
		try:
			user_id=s.loads(token)["user_id"]
		except:
			return None
		return User.query.get(user_id)
	
	
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
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	email=db.Column(db.String(50),nullable=False)
	replies=db.relationship("Reply",backref="replied")
	post_id=db.Column(db.Integer,db.ForeignKey("post.id"))



class Reply(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(50),nullable=False)
	comment=db.Column(db.Text,nullable=False)
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	email=db.Column(db.String(50),nullable=False)
	comment_id=db.Column(db.Integer,db.ForeignKey("comment.id"))
