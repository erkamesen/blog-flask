from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    text = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")