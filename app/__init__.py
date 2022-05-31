from flask import Flask, render_template, request, flash, url_for, redirect
from flask_mysqldb import MySQL
import mysql.connector

from .prueba import insertBLOB
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
app_root = os.path.dirname(os.path.abspath(__file__))

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
        return render_template('admin.html', rows=row)
    except Exception as ex:
        raise Exception(ex)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    target = os.path.join(app_root, './static/images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    if request.method == 'POST':
        try:
            id_prod = request.form['idProducto']
            id_prod = int(id_prod)
            nombre = request.form['nombre']
            precio = request.form['precio']
            precio = float(precio)
            descripcion = request.form['descripcion']
            id_cate = request.form['categoria']
            id_cate = int(id_cate)
            id_cat = request.form['catalogo']
            id_cat = int(id_cat)
            id_est_prod = request.form['estadoProducto']
            id_est_prod = int(id_est_prod)
            files = request.files.getlist("imagen")
            file_name = ''
            for file in files:
                file_name = file.filename
                destination = '/'.join([target, file_name])
                file.save(destination)
            insertBLOB(id_prod, nombre, precio, descripcion,
                       destination, id_cate, id_cat, id_est_prod)

            cursor = db.connection.cursor()
            sql = "SELECT * FROM productos"
            cursor.execute(sql)
            row = cursor.fetchall()
            return render_template('admin.html', rows=row)
        except Exception as exc:
            raise Exception(exc)
    else:
        return render_template('agregar.html')


@app.route('/eliminar')
def eliminar():
    try:
        cursor = db.connection.cursor()
        sql = "SELECT id_producto, nombre FROM productos"
        cursor.execute(sql)
        row = cursor.fetchall()
        return render_template('eliminar.html', rows=row)
    except Exception as ex:
        raise Exception(ex)


@app.route('/eliminar/<int:id>',  methods=['GET'])
def eliminarid(id):
    try:
        cursor = db.connection.cursor()
        sql = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(sql,[id])
        db.connection.commit()
        cursor = db.connection.cursor()

        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        row = cursor.fetchall()
        return render_template('admin.html', rows=row)
    except Exception as ex:
        raise Exception(ex)


@app.route('/modificar')
def modificar():
    return render_template('modificar.html')


def inicializarApp(config):
    app.config.from_object(config)
    return app
