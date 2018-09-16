"""
Contains all forms for blogfolio
"""
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class ContactForm(Form):
    name = StringField('name', validators=[DataRequired()])
    mail = StringField('mail', validators=[DataRequired()])
    msg = TextAreaField('msg', validators=[DataRequired()])
