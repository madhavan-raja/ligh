import os
import secrets
from PIL import Image
from flask import current_app

def save_post_picture(post_picture):
    random_hex = secrets.token_hex(8)
    _, fileext = os.path.splitext(post_picture.filename)
    post_picture_filename = random_hex + fileext
    picture_path = os.path.join(current_app.root_path, 'static/userdata/post_pics', post_picture_filename)

    output_size = (1900, 1500)
    img = Image.open(post_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return post_picture_filename