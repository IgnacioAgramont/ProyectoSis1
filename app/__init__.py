from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from config import config
from .models.ModelUser import ModelUser
from .models.entities.user import User

app = Flask(__name__)

# SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost:3306/proyectosis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dbalchemy = SQLAlchemy(app)

# Fin SQLALchemy


db = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/sucursales')
def sucursales():
    return render_template('sucursales.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['user'])
        # print(request.form['password'])

        user = User(0, request.form['user'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('admin'))
            else:
                flash("Password incorrecto")
            return render_template('login.html')
        else:
            flash("Usuario no encontrado")
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/admin')
def admin():
    try:
        cursor = db.connection.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        row = cursor.fetchall()
        return render_template('admin.html', rows = row)
    except Exception as ex:
        raise Exception(ex)
    


@app.route('/agregar')
def agregar():
    try:
        cursor = db.connection.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        row = cursor.fetchall()
        return render_template('agregar.html')
    except Exception as ex:
        raise Exception(ex)
    


@app.route('/eliminar')
def eliminar():
    return render_template('eliminar.html')


@app.route('/modificar')
def modificar():
    return render_template('modificar.html')


def inicializarApp(config):
    app.config.from_object(config)
    return app
