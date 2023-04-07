from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100, message='Длина пароля от 4 до 100 символов')])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Имя: ', validators=[Length(min=4, max=15, message='Имя должно быть от 4 до 15 символов')])
    email = StringField('Email: ', validators=[Email('некорректный email')])
    psw = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=20, message='пароль должен содержать от 4 до 20 символов')])
    psw2 = PasswordField('Повтор пароля: ', validators=[DataRequired(), EqualTo('psw', message='пароли не совпадают')])
    submit = SubmitField('Регистрация')