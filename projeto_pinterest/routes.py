#Crias as rotas do nosso site (os links)

from flask import render_template, url_for, redirect, request
from projeto_pinterest import app, database, bcrypt
from projeto_pinterest.models import Usuario, Posts
from flask_login import login_required, login_user, logout_user, current_user
from projeto_pinterest.forms import FormLogin, FormCriarConta, FormFoto
from flask_wtf import FlaskForm
from wtforms import FileField
import pathlib
from werkzeug.utils import secure_filename
from . import PathUtils
from . import utils

#* Criando a home page do site
@app.route("/", methods= ["GET", "POST"])
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form= formlogin)

@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) #Criptografar senha do usuario
        usuario = Usuario(username=form_criarconta.username.data,
                        email=form_criarconta.email.data,
                        senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criar_conta.html", form=form_criarconta)

#* Criando a página de perfil dos usuarios
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required  # Para garantir que apenas usuarios logados acessem a página do perfil
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id): # O usuario está vendo o próprio perfil 
        form_foto = FormFoto()
        if request.method == "POST":
            if form_foto.validate_on_submit():
                photo_field: FileField = form_foto.foto
                arquivo = photo_field.data
                *filename, ext = arquivo.filename.split('.')
                filename = ".".join(filename)
                nome_seguro = utils.hash(filename)
                nome_seguro += "." + ext
                #* Salvar arquivo na pasta fotos post
                file_path: pathlib.Path = PathUtils.UPLOAD_DIR.value / pathlib.Path(nome_seguro)
                # caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                #                         app.config["UPLOAD_FOLDER"], nome_seguro)
                
                #* Registrar o arquivo no banco de dados
                if not file_path.exists():
                    arquivo.save(file_path)
                    foto = Posts(imagem=nome_seguro , id_usuario =current_user.id )
                    database.session.add(foto)
                    database.session.commit()
                    database.session.flush(foto)
                    print(file_path)
                else:
                    print("Arquivo ja existe")
            return render_template("perfil.html", usuario= current_user,form = form_foto)
        elif request.method == "GET":
            return render_template("perfil.html", usuario= current_user,form = form_foto)
    else:
        usuario= Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required # Para garantir que apenas usuarios logados acessem a página do feed
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required  # Para garantir que apenas usuarios logados acessem a página do feed
def feed():
    fotos= Posts.query.order_by(Posts.data_de_criação).all()
    return render_template("feed.html", fotos=fotos)