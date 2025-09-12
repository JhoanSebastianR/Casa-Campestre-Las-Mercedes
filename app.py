from flask import Flask, jsonify
from flask import flash, get_flashed_messages # se importan para poder enviar mensajes a sweetAlerte2
from flask import render_template, request, redirect, session
from flask import url_for
from flask import request                 #recepciona la informacion "DEL FORMULARIO"
from flask import redirect                #redirecciona "MUESTRA LA INFORMACION PARA LAS TABLAS"
import mysql.connector                    #Se importa libreria para conexion a base de datos 
from datetime import datetime             #Se importa para colocar un tiempo exacto "Para la imagen"
from flask import send_from_directory     #optenemos informacion de la imagen
from flask import abort #obtenemos la informacion de la imagen, es necesaria para mostrar las imagenes
import os

app = Flask(__name__)
app.secret_key = "Connor2018"  # Necesario para usar flash

# Configuración de la conexión MySQL
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'database': 'casa_campestre'
}

@app.route('/')
def inicio():
    return render_template('sitio/index.html')


@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')


@app.route('/admin/')
def admin():
    if not 'login' in session:
      return redirect('/admin/login')

    return render_template('admin/index.html')


# Login

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')



@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    print(_usuario)
    print(_password)

    if _usuario == 'admin' and _password == 'Connor2018':
        session['login'] = True
        session['usuario'] = "Administrador"
        return redirect('/admin')
    
    return render_template('admin/login.html')

@app.route('/admin/cerrar')
def admin_cerrar():
    session.clear()
    return redirect('/admin/login')

# Cliente

@app.route('/admin/cliente')
def admin_cliente():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `cliente`")
    cliente = cursor.fetchall()
    conexion.commit()
    print(cliente)
    

    return render_template('admin/cliente.html', cliente=cliente)

@app.route('/admin/cliente/guardar', methods=['POST'])
def admin_cliente_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

    
    id_cliente = request.form['id_cliente']
    nombre_cliente = request.form['nombre_cliente']
    apellido_cliente = request.form['apellido_cliente']
    sexo_cliente = request.form['sexo_cliente']
    telefono_cliente = request.form['telefono_cliente']
    direccion_cliente = request.form['direccion_cliente']

    sql = "INSERT INTO cliente (id_cliente, nombre, apellido, sexo, telefono, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (id_cliente, nombre_cliente, apellido_cliente, sexo_cliente, telefono_cliente, direccion_cliente)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_cliente)
    print(nombre_cliente)
    print(apellido_cliente)
    print(sexo_cliente)
    print(telefono_cliente)
    print(direccion_cliente)


    return redirect('/admin/cliente')

@app.route('/admin/cliente/borrar', methods=['POST'])
def admin_cliente_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `cliente` WHERE id_cliente=%s", (_id,))
    cliente = cursor.fetchall()
    conexion.commit()
    print(cliente)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (_id,))
    conexion.commit()

    return redirect('/admin/cliente')

# Casa

@app.route('/admin/casa')
def admin_casa():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `casa`")
    casa = cursor.fetchall()
    conexion.commit()
    print(casa)


    return render_template('admin/casa.html', casa=casa)


@app.route('/admin/casa/guardar', methods=['POST'])
def admin_casa_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

    
    id_casa = request.form['id_casa']
    nom_casa = request.form['nom_casa']
    radio_perimetro = request.form['radio_perimetro']


    sql = "INSERT INTO `casa` (`id_casa`, `nom_casa`, `radio_perimetro`) VALUES (%s, %s, %s)"
    datos = (id_casa, nom_casa, radio_perimetro)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_casa)
    print(nom_casa)
    print(radio_perimetro)
   

    return redirect('/admin/casa')

@app.route('/admin/casa/borrar', methods=['POST'])
def admin_casa_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    

    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `casa` WHERE id_casa=%s", (_id,))
    casa = cursor.fetchall()
    conexion.commit()
    print(casa)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM casa WHERE id_casa=%s", (_id,))
    conexion.commit()

    return redirect('/admin/casa')


# Tipo_producto


@app.route('/admin/tipo_producto')
def admin_tipo_producto():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `tipo_producto`")
    tipo_producto = cursor.fetchall()
    conexion.commit()
    print(tipo_producto)


    return render_template('admin/tipo_producto.html', tipo_producto=tipo_producto)


@app.route('/admin/tipo_producto/guardar', methods=['POST'])
def admin_tipo_producto_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    id_tipoproducto = request.form['id_tipoproducto']
    descripcion = request.form['descripcion']


    sql = "INSERT INTO `tipo_producto` (`id_tipoproducto`, `descripcion`) VALUES (%s, %s)"
    datos = (id_tipoproducto, descripcion)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_tipoproducto)
    print(descripcion)
   

    return redirect('/admin/tipo_producto')

@app.route('/admin/tipo_producto/borrar', methods=['POST'])
def admin_tipo_producto_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `tipo_producto` WHERE id_tipoproducto=%s", (_id,))
    tipo_producto = cursor.fetchall()
    conexion.commit()
    print(tipo_producto)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `tipo_producto` WHERE id_tipoproducto=%s", (_id,))
    conexion.commit()

    return redirect('/admin/tipo_producto')


if __name__ == '__main__':
    app.run(debug=True)