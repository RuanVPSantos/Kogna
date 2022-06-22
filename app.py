import os
import unicodedata
import bcrypt

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from random import randrange

def create_app():
    
    app = Flask(__name__)
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    db = SQL("sqlite:///data.db")
    
    @app.route('/')
    def index(problema=''):
        try:
            usuario_todos_os_dados = db.execute('select * from users where id = (?)', session['user'])[0]
            adm = False
            if usuario_todos_os_dados['adm'] == True:
                adm = True
            usuario = usuario_todos_os_dados['username']
            return render_template('index.html', user=usuario, adm=adm)
        except:
            return render_template("index.html")
    
    @app.route('/login', methods=["POST", 'GET'])
    def login():
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password').encode('utf-8')
            try:
                usuario = db.execute("SELECT * FROM users WHERE username = (?)", username)[0]
            except:
                return render_template('index.html', problema='Usuário não encontrado')        
            
            if not (bcrypt.checkpw(password, usuario['password'])):
                return render_template('index.html', problema='Senha não condizente, favor rever')
            
            session['user'] = usuario['id']
            
            return redirect('/')      
    
    @app.route('/sign_up', methods=['GET', 'POST'])
    def sign_up():
        if request.method == "GET":
            redirect('/')
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            tel = request.form.get('tel')
            password = request.form.get('password')
            confpassword = request.form.get("confirm-password")
            
        if not username or not email or not tel or not password or not confpassword:
            return render_template('index.html', problema='Dados faltantes')
        if password != confpassword:
            return render_template('index.html', problema ='As senhas não coincidem')
        try: 
            tel = int(tel)
        except: 
            return render_template('index.html', problema ='Telefone inválido')
        if not (int(tel/10**10) > 0) or not (int(tel/10**11) == 0) or (int((tel%10**9)/10**8)==0):
            return render_template('index.html', problema ='Telefone inválido')
        
        repetidos = db.execute('SELECT * FROM users WHERE username = (?) OR email = (?) OR tel = (?)', username, email, tel)
        
        if len(repetidos) > 0:
            return render_template('index.html', problema='dados já cadastrados')
        
        hashpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        db.execute('''
                   INSERT INTO users(username, password, email, confirmed, tel, adm) VALUES (?,?,?,?,?,?)
                   ''', username, hashpassword, email, False, tel,False)
        
        return render_template('index.html', problema = 'dados cadastrados com sucesso')
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    
    return app