from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=140)])
    content = TextAreaField('Content (Markdown)', validators=[DataRequired()])
    submit = SubmitField('Submit')