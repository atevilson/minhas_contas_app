from flask_wtf import FlaskForm 
from wtforms import (
    StringField, PasswordField, SubmitField,
    DateField, FloatField, SelectField, IntegerField
)
from wtforms.validators import DataRequired, Length
from wtforms.validators import InputRequired, NumberRange, Length

class RegistrationForm(FlaskForm):
    username = StringField('Usuário',
        validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Senha',
        validators=[DataRequired(), Length(min=6)])
    submit   = SubmitField('Cadastre-se')

class LoginForm(FlaskForm):
    username = StringField('Usuário',
        validators=[DataRequired()])
    password = PasswordField('Senha',
        validators=[DataRequired()])
    submit   = SubmitField('Entrar')

class ExpenseForm(FlaskForm):
    origem     = StringField('Origem', validators=[DataRequired()])
    vencimento = DateField('Vencimento',
        format='%Y-%m-%d', validators=[DataRequired()])
    valor      = FloatField('Valor', validators=[DataRequired()])
    status     = SelectField('Status',
        choices=[('Pago','Pago'),('A pagar','A pagar')])
    quem_paga  = StringField('Quem paga')
    tipo       = SelectField('Tipo',
        choices=[('Fixa','Fixa'),('A prazo','A prazo')])
    parcelas   = IntegerField('Número de parcelas', default=1,
        validators=[InputRequired(message="Informe 0 ou mais parcelas"), NumberRange(min=0, message="Não pode ser negativo")])
    submit     = SubmitField('Salvar')