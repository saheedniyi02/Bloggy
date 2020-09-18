
import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from blog import mail
def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex+f_ext
	picture_path=os.path.join(current_app.root_path,"static/profile_pics",picture_fn)
	
	output_size=(150,150)
	i=Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn
	
	
def send_request_email(user):
	token=user.get_reset_token()
	msg=Message("User Passsord Reset",sender="nooreply@gmail.com",recipients=[user.email])
	msg.body=f'''Password Reset Email
To reset your password,kindly click the attached link
	{url_for("users.resetpassword",token=token,_external=True)}
	
	
	Thank you!!
	'''
	mail.send(msg)