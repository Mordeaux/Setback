from wtforms import Form, TextField, PasswordField, validators
# possibly add more wtforms stuff later? or just do it myself bc ajax
#from wtforms.ext.sqlalchemy.orm import model_form

class LoginForm(Form):
    username = TextField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.Required(),
    ])

