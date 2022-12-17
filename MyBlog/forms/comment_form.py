from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")
