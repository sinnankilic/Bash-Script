from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Parola', validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField('Kayıt Ol')

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Parola', validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField('Giriş Yap')
