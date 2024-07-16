# Criar formularios no nosso site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from projeto_pinterest.models import Usuario


#Classe para o login da conta do usuario através de um formulário
class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("E-mail inexistente, Crie uma conta.")


#Classe para criação da conta do usuario através de um formulário
class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de senha", validators=[DataRequired(),EqualTo('senha')])
    botao_confirmacao = SubmitField("Criar conta")

    #Validar se o e-mail já existe no banco de dados
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado, faça o login para continuar.")
        
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators= [DataRequired()])
    botao_confirmacao = SubmitField("Enviar")