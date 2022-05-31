from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_mysqldb import MySQL
import mysql.connector

from .prueba import insertBLOB, readBLOB, insertPedido
import os
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/productos')
def productos():
    try:
        cursor = db.connection.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        row = cursor.fetchall()
        rowfinal = []
        rowaux = []
        for productos in row:
            rowaux.append(productos[0])
            rowaux.append(productos[1])
            rowaux.append(productos[2])
            rowaux.append(productos[3])
            rowaux.append(readBLOB(productos[0]))
            rowaux.append(productos[5])
            rowaux.append(productos[6])
            rowaux.append(productos[6])
            aux = tuple(rowaux)
            # print(aux)
            rowfinal.append(aux)
            rowaux = []
        # print('-------------------------------final----------------------')
        rowfinal = tuple(rowfinal)
        # print(rowfinal)
        # for productos in row:
        #     imagen1 = productos[4]
        #     # The returned data will be a list of list
        #     image = imagen1[0][0]

        #     # Decode the string
        #     binary_data = base64.b64decode(image)

        #     # Convert the bytes into a PIL image
        #     image = Image.open(io.BytesIO(binary_data))

        #     # Display the image
        #     image.show()
        return render_template('productos.html', rows=rowfinal)
    except Exception as ex:
        raise Exception(ex)


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

@app.route('/pedido_confirmado',methods=['GET', 'POST'])
def pedido_confirmado():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            nit = request.form['nit']
            
            insertPedido(nombre, apellido, direccion, telefono, nit)

            session['cart'] = []
            session.modified = True

            cursor = db.connection.cursor()
            sql = "SELECT * FROM productos"
            cursor.execute(sql)
            row = cursor.fetchall()
            return render_template('index.html', rows=row)
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
        cursor.execute(sql, [id])
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


@app.route('/cart_add', methods=['GET', 'POST'])
def cart_add():
    if request.method == 'POST':
        if 'cart' not in session:
            session['cart'] = []
            return redirect(url_for('productos'))
        # print(request.form.get("id_producto"))
        # print(request.form.get("nombre"))
        # print(request.form.get("precio"))
        # print(request.form.get("img"))
        session['cart'].append(
            {'id': request.form.get("id_producto"), 'nombre': request.form.get(
                "nombre"), 'cantidad': request.form.get("cantidad"), 'precio': request.form.get("precio"), 'img': request.form.get("img")})
        session.modified = True

        return redirect(url_for('productos'))
    else:
        return redirect(url_for('productos'))


def carrito():

    productos = []
    total = 0.0
    indice = 0
    cantidad_total = 0
    total_final = 0.0

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='proyectosis',
                                             user='root',
                                             password='')

        for item in session['cart']:
            cursor = connection.cursor()
            sql_fetch_blob_query = "SELECT * from productos where id_producto = %s"
            cursor.execute(sql_fetch_blob_query, [item['id']])
            producto = cursor.fetchone()
            cantidad = int(item['cantidad'])
            total = cantidad * int(producto[2])
            total_final += total

            cantidad_total += cantidad

            productos.append({'id_producto': producto[0], 'nombre': producto[1], 'precio': float(producto[2]),
                             'imagen': item['img'], 'cantidad': cantidad, 'total': total, 'indice': indice})
            indice += 1
        total_envio = total_final + 10

        return productos, float(total_final), float(total_envio), cantidad_total

    except mysql.connector.Error as error:
        print("Fallo {}".format(error))

@app.route('/quitar_del_cart/<index>')
def quitar_del_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    productos, parcial, total, cantidad_total = carrito()
    # print('---------------------------productos---------------------')
    # print(productos)
    # print('---------------------------parcial---------------------')
    # print(parcial)
    # print('---------------------------total---------------------')
    # print(total)
    # print('---------------------------cantidad_total---------------------')
    # print(cantidad_total)
    return render_template('cart.html', productos = productos, parcial = parcial, total = total, cantidad_total = cantidad_total)


def inicializarApp(config):
    app.config.from_object(config)
    return app
