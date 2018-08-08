from wtforms import Form
from wtforms.validators import Required, Length, EqualTo, Email
import wtforms


class SignUpForm(Form):
    username = wtforms.StringField(validators=[
        Required(),
        Length(max=20)
    ])
    email = wtforms.StringField(validators=[Email(), Required()])
    password = wtforms.PasswordField(validators=[Required()])
    password_repeat = wtforms.PasswordField(validators=[
        Required(), 
        EqualTo('password', message='Password must match')
    ])

class LogInForm(Form):
    email = wtforms.StringField(validators=[Email(), Required()])
    password = wtforms.PasswordField(validators=[Required()])