from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, URL

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")