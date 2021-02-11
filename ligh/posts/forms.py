from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    post_picture = FileField('Post Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    use_default_post_picture = BooleanField()
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
