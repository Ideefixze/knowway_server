from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class FindWikipediaForm(FlaskForm):
    searchWiki = StringField('Find article:', validators=[DataRequired()])
    submit = SubmitField('Search')

class FindPolonaForm(FlaskForm):
    searchPolona = StringField('Find Polona book:', validators=[DataRequired()])
    submit = SubmitField('Search')

class AddCommentForm(FlaskForm):
    content = TextAreaField('', validators=[DataRequired()],render_kw={'style':'resize:none; width:144px; height:64px;'})
    submit = SubmitField('Add comment')