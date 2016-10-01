from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField
from wtforms.validators import Required, Length


class RegisterForm(Form):
    unit_choices = [
            ('B', 'BTC'), 
            ('m', 'mBTC'), 
            ('u', 'Bits')
    ]

    currencies = [
            ('USD', 'USD'),
            ('GBP', 'GBP'),
            ('EUR', 'EUR'),
    ]
    unit_field = SelectField(
            u'Preferred Coin Units', 
            choices = unit_choices,
            validators = [Required()])

    fiat_field = SelectField(
            u'Preferred Currency Conversion',
            choices = currencies,
            validators = [Required()])


