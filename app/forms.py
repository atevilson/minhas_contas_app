from flask_wtf import FlaskForm 
from wtforms import (
    StringField, PasswordField, SubmitField,
    DateField, SelectField, IntegerField,
    DecimalField
)
from wtforms.validators import DataRequired, Length, InputRequired, NumberRange, EqualTo
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
    valor      = DecimalField('Valor', places=2, validators=[InputRequired(message="Informe um valor válido"), 
        NumberRange(min=1, message="Não pode ser negativo")])
    status     = SelectField('Status',
        choices=[('Pago','Pago'),('A pagar','A pagar')])
    quem_paga  = StringField('Quem paga')
    tipo       = SelectField('Tipo',
        choices=[('Fixa','Fixa'),('A prazo','A prazo')])
    parcelas   = IntegerField('Número de parcelas', default=1,
        validators=[InputRequired(message="Informe 0 ou mais parcelas"), NumberRange(min=0, message="Não pode ser negativo")])
    submit     = SubmitField('Salvar')

class ResetPasswordForm(FlaskForm):
    username        = StringField('Usuário', validators=[DataRequired()])
    new_password    = PasswordField('Nova senha', validators=[DataRequired()])
    confirm_password= PasswordField(
        'Confirmar senha',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='As senhas devem coincidir.')
        ]
    )
    submit = SubmitField('Cadastrar')