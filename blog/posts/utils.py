from flask import url_for
from flask_mail import Message
from blog import mail
from blog.models import Post,Comment

def send_comment_email(id,new_comment):
	post=Post.query.get(id)
	author_email=post.author.email
	msg=Message("Comment Notification from blogIt",sender="noreply@gmail.com",recipients=[author_email])
	msg.body=f"""
Someone Commented on your post on Blogit.
{url_for("posts.post",id=post.id,_external=True)}.
{new_comment.comment[0:int(len(new_comment.comment)/3)]}
	"""
	mail.send(msg)

	
	
def send_reply_email(id,new_reply):
	comment=Comment.query.get(id)
	replies=Reply.query.filter_by(replied=comment).all()
	email_commenter=[comment.email]
	email_of_previously_replied=[]
	if replies:
		for reply in replies:
			if reply.email !="AnonymousUser":
				email_of_previously_replied.append(reply.email)
		msg_repliers=Message("Notification From Blog It",sender="noreply@gmail.com",recipients=email_of_previously_replied)
		msg_repliers.body=f'''Someone also replied to a post you replied to. 
		{url_for("posts.comment_replies",id=id,_external=True)}

{new_reply.comment[0:int(len(new_reply.comment)/3)]}
			
		
		
		
		
		'''
		
	msg_commenter=Message("Notification From Blog It",sender="noreply@gmail.com",recipients=email_commenter)
	msg_commenter.body=f'''
Someone replied to a comment you made on blogit
'{url_for("posts.comment_replies",id=id,_external=True)}'

{new_reply.comment[0:int(len(new_reply.comment)/3)]}
	
	'''
	mail.send(msg_commenter)
	
