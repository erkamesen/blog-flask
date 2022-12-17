from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
