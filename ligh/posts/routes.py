from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from ligh import db
from ligh.models import Post
from ligh.posts.forms import PostForm
from ligh.posts.utils import save_post_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.use_default_post_picture.data:
            post_picture_filename = "default.jpg"
        elif form.post_picture.data:
            post_picture_filename = save_post_picture(form.post_picture.data)
        else:
            post_picture_filename = "default.jpg"
        post = Post(title=form.title.data, subtitle=form.subtitle.data, post_picture=post_picture_filename, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New post created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        if form.use_default_post_picture.data:
            post.post_picture = "default.jpg"
        elif form.post_picture.data:
            post_picture_filename = save_post_picture(form.post_picture.data)
            post.post_picture = post_picture_filename
        post.content = form.content.data
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('main.home'))
