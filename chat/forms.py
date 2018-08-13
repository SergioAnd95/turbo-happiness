from wtforms import Form
from wtforms.validators import Required, Length, EqualTo, Email
import wtforms


class ChatCreateForm(Form):
    name = wtforms.StringField(validators=[
        Required(),
        Length(max=20)
    ])