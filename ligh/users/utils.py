import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from ligh import mail


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, fileext = os.path.splitext(form_picture.filename)
    profile_picture_filename = random_hex + fileext
    picture_path = os.path.join(current_app.root_path, 'static/userdata/profile_pics', profile_picture_filename)

    output_size = (1900, 1500)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return profile_picture_filename


def send_reset_email(user):
    token = user.get_reset_token
    msg = Message('Password Reset Request', sender='noreply@flaskblog.com', recipients=[user.email])
    msg.body = f"""Visit the following link to reset the password:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this message.
"""
    mail.send(msg)

