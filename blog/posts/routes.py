from flask import Blueprint,abort,request,url_for,flash,redirect,render_template
from flask_login import current_user,login_required
from blog import db
from blog.models import User,Comment,Post,Reply
from blog.posts.forms import PostForm,CommentFormCurrent,CommentFormAnonymous
from blog.posts.utils import send_comment_email,send_reply_email
posts=Blueprint("posts",__name__)

@posts.route("/newpost",methods=["GET","POST"])
@login_required
def create_post():
	form=PostForm()
	if form.validate_on_submit():
		post=Post(title=form.title.data,content=form.content.data,brief=form.content.data[:int(len(form.content.data)/6)],author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("Your post has been created","success")
		return redirect(url_for("main.home"))
	return render_template("create_post.html",form=form,legend="Create Post")


@posts.route("/post/update/<int:id>",methods=["POST","GET"])
@login_required
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
		return redirect(url_for('posts.post',id=post.id))
	elif request.method=="GET":
		form.title.data=post.title
		form.content.data=post.content
	return render_template("create_post.html",form=form,legend="Update Post")
	
	


@posts.route("/post/<int:id>")
def post(id):
	post=Post.query.get_or_404(id)
	comments=Comment.query.filter_by(topic=post).order_by(Comment.date_posted.desc()).all()
	return render_template("post.html",post=post,comments=comments,Reply=Reply,Comment=Comment)


@posts.route("/post/delete/<int:id>",methods=["POST","GET"])
@login_required
def delete_post(id):
		post=Post.query.get_or_404(id)
		if post.author!=current_user:
			abort(403)
		db.session.delete(post)
		db.session.commit()
		return redirect(url_for("main.home"))
		
@posts.route("/comment/<int:post_id>",methods=["GET","POST"])
def comment(post_id):
	post=Post.query.get(post_id)
	if current_user.is_authenticated:
			form=CommentFormCurrent()
			if form.validate_on_submit():
				comment=Comment(name=current_user.username,email=current_user.email,comment=form.comment.data,topic=post)
				db.session.add(comment)
				db.session.commit()
				send_comment_email(post_id,comment)
				return redirect(url_for("posts.post",id=post.id))
	else:
			form=CommentFormAnonymous()
			if form.validate_on_submit():
				comment=Comment(name=form.email.data[0:6]+"...@"+form.email.data.split("@")[-1],email=form.email.data,comment=form.comment.data,topic=post)
				db.session.add(comment)
				db.session.commit()
				send_comment_email(post_id,comment)
				return redirect(url_for("posts.post",id=post.id))
	return render_template("comment.html",form=form,legend="Comment")
	
	
@posts.route("/reply/<int:comment_id>",methods=["GET","POST"])
def reply(comment_id):
	comment=Comment.query.get(comment_id)
	if current_user.is_authenticated:
			form=CommentFormCurrent()
			if form.validate_on_submit():
				reply=Reply(name=current_user.username,email=current_user.email,comment=form.comment.data,replied=comment)
				db.session.add(reply)
				db.session.commit()
				send_reply_email(comment_id,reply)
				return redirect(url_for("posts.comment_replies",id=reply.replied.id))	
	else:
			form=CommentFormAnonymous()
			if form.validate_on_submit():
				reply=Reply(name=form.email.data[0:6]+"...@"+form.email.data.split("@")[-1],email=form.email.data,comment=form.comment.data,replied=comment)
				db.session.add(reply)
				db.session.commit()
				send_reply_email(comment_id,reply)
				return redirect(url_for("posts.comment_replies",id=reply.replied.id))		
	return render_template("comment.html",form=form,legend="Reply",comment=comment)
	


	
@posts.route("/viewreplies/<int:id>/")
def comment_replies(id):
	comment=Comment.query.get(id)
	replies=Reply.query.filter_by(replied=comment).order_by(Reply.date_posted.desc()).all()
	return render_template("replies.html",comment=comment,replies=replies)
	
	
