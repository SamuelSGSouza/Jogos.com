from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo
from flask_mysqldb import MySQL
from dao import JogoDao, UsuarioDao
import os





app = Flask(__name__)
app.secret_key = "samuca"

app.config['MYSQL_USER'] = 'root'
app.config["MYSQL_PASSWORD"] = 'admin'
app.config["MYSQL_DB"] = 'jogoteca'
app.config["UPLOAD_PATH"] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo="Jogos", jogos=lista)

@app.route('/novo')
def jogo_novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for('login', proxima=url_for('jogo_novo')))
    return render_template("novo.html", titulo="Jogo_Novo")

@app.route('/criar', methods=["POST",])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)
    imagem = request.files["arquivo"]
    imagem.save(f"{app.config['UPLOAD_PATH']}/capa{jogo.id}.jpg")
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=["POST", "GET"],)
def autenticando():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session["usuario_logado"] = usuario.id
            flash(usuario.nome + " logou com sucesso!")
            session["usuario_logado"] = request.form["usuario"]
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Login falhou...')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    return render_template("editar.html", titulo="editando jogo", jogo=jogo, capa=f'capa{id}.jpg' )


@app.route('/atualizar', methods=["POST",])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash("O jogo foi removido com sucesso")
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)







app.run(debug=True)