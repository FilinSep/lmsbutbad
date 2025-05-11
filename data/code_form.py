from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField

class CodeForm(FlaskForm):
    code = TextAreaField()
    submit = SubmitField('Отправить код')