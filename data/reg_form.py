from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')