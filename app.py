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


def get_db():
    """Helper que devuelve una conexión MySQL usando la configuración global.
    Recuerda cerrar la conexión cuando ya no se necesite (conexion.close()).
    """
    return mysql.connector.connect(**config)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')


@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/alquiler')
def alquiler():
    return render_template('sitio/alquiler.html')

@app.route('/pasadia')
def pasadia():
    return render_template('sitio/pasadia.html')

@app.route('/eventos')
def eventos():
    return render_template('sitio/eventos.html')


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

    conexion = get_db()
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
    conexion = get_db()
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

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `cliente` WHERE id_cliente=%s", (_id,))
    cliente = cursor.fetchall()
    conexion.commit()
    print(cliente)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM cliente WHERE id_cliente=%s", (_id,))
    conexion.commit()

    return redirect('/admin/cliente')

# Casa

@app.route('/admin/casa')
def admin_casa():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
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
    conexion = get_db()
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

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `casa` WHERE id_casa=%s", (_id,))
    casa = cursor.fetchall()
    conexion.commit()
    print(casa)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM casa WHERE id_casa=%s", (_id,))
    conexion.commit()

    return redirect('/admin/casa')


# Tipo_producto


@app.route('/admin/tipo_producto')
def admin_tipo_producto():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
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
    conexion = get_db()
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

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `tipo_producto` WHERE id_tipoproducto=%s", (_id,))
    tipo_producto = cursor.fetchall()
    conexion.commit()
    print(tipo_producto)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `tipo_producto` WHERE id_tipoproducto=%s", (_id,))
    conexion.commit()

    return redirect('/admin/tipo_producto')


# Propietario


@app.route('/admin/propietario')
def admin_propietario():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `propietario`")
    propietario = cursor.fetchall()
    conexion.commit()
    print(propietario)


    return render_template('admin/propietario.html', propietario=propietario)


@app.route('/admin/propietario/guardar', methods=['POST'])
def admin_propietario_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    id_propietario = request.form['id_propietario']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    sexo = request.form['sexo']
    id_casa = request.form['id_casa']



    sql = "INSERT INTO `propietario` (`id_propietario`, `nombre`, `apellido`, `sexo`, `id_casa`) VALUES (%s, %s, %s, %s, %s)"
    datos = (id_propietario, nombre, apellido, sexo, id_casa)
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_propietario)
    print(nombre)
    print(apellido)
    print(sexo)
    print(id_casa)
   

    return redirect('/admin/propietario')

@app.route('/admin/propietario/borrar', methods=['POST'])
def admin_propietario_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `propietario` WHERE id_propietario=%s", (_id,))
    propietario = cursor.fetchall()
    conexion.commit()
    print(propietario)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `propietario` WHERE id_propietario=%s", (_id,))
    conexion.commit()

    return redirect('/admin/propietario')



# Factura


@app.route('/admin/factura')
def admin_factura():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM `factura`")
    factura = cursor.fetchall()
    conexion.commit()
    print(factura)

    cursor.execute("SELECT * FROM `producto`")
    productos = cursor.fetchall()
    conexion.commit()
    




    return render_template('admin/factura.html', factura=factura ,  productos = productos)


@app.route('/admin/factura/guardar', methods=['POST'])
def admin_factura_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    numero_factura = request.form['numero_factura']
    id_producto = request.form['id_producto']
    id_propietario = request.form['id_propietario']
    id_cliente = request.form['id_cliente']
    cantidad = request.form['cantidad']
    valor_venta = request.form['valor_venta']
    fecha_venta = request.form['fecha_venta']



    sql = "INSERT INTO `factura` (`numero_factura`, `id_producto`, `id_propietario`, `id_cliente`, `cantidad`, `valor_venta`, `fecha_venta`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    datos = (numero_factura, id_producto, id_propietario, id_cliente, cantidad, valor_venta, fecha_venta)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(numero_factura)
    print(id_producto)
    print(id_propietario)
    print(id_cliente)
    print(cantidad)
    print(valor_venta)
    print(fecha_venta)
   

    return redirect('/admin/factura')

@app.route('/admin/factura/borrar', methods=['POST'])
def admin_factura_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `factura` WHERE numero_factura=%s", (_id,))
    factura = cursor.fetchall()
    conexion.commit()
    print(factura)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `factura` WHERE numero_factura=%s", (_id,))
    conexion.commit()

    return redirect('/admin/factura')







# Producto


@app.route('/admin/producto')
def admin_producto():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `producto`")
    producto = cursor.fetchall()
    conexion.commit()
    print(producto)


    return render_template('admin/producto.html', producto=producto)


@app.route('/admin/producto/guardar', methods=['POST'])
def admin_producto_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    id_producto = request.form['id_producto']
    id_tipoproducto = request.form['id_tipoproducto']
    descripcion = request.form['descripcion']
    valor_venta = request.form['valor_venta']
    valor_compra = request.form['valor_compra']



    sql = "INSERT INTO `producto` (`id_producto`, `id_tipoproducto`, `descripcion`, `valor_venta`, `valor_compra`) VALUES (%s, %s, %s, %s, %s)"
    datos = (id_producto, id_tipoproducto, descripcion, valor_venta, valor_compra)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_producto)
    print(id_tipoproducto)
    print(descripcion)
    print(valor_venta)
    print(valor_compra)
   

    return redirect('/admin/producto')

@app.route('/admin/producto/borrar', methods=['POST'])
def admin_producto_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `producto` WHERE id_producto=%s", (_id,))
    producto = cursor.fetchall()
    conexion.commit()
    print(producto)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `producto` WHERE id_producto=%s", (_id,))
    conexion.commit()

    return redirect('/admin/producto')





# Inventario


@app.route('/admin/inventario')
def admin_inventario():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `inventario`")
    inventario = cursor.fetchall()
    conexion.commit()
    print(inventario)


    return render_template('admin/inventario.html', inventario=inventario)


@app.route('/admin/inventario/guardar', methods=['POST'])
def admin_inventario_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    id_inventario = request.form['id_inventario']
    fecha_inventario = request.form['fecha_inventario']
    id_producto = request.form['id_producto']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']



    sql = "INSERT INTO `inventario` (`id_inventario`, `fecha_inventario`, `id_producto`, `cantidad`, `ubicacion`) VALUES (%s, %s, %s, %s, %s)"
    datos = (id_inventario, fecha_inventario, id_producto, cantidad, ubicacion)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_inventario)
    print(fecha_inventario)
    print(id_producto)
    print(cantidad)
    print(ubicacion)
   

    return redirect('/admin/inventario')

@app.route('/admin/inventario/borrar', methods=['POST'])
def admin_inventario_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    
    _id = request.form['txtID']
    print(_id)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `inventario` WHERE id_inventario=%s", (_id,))
    inventario = cursor.fetchall()
    conexion.commit()
    print(inventario)

    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `inventario` WHERE id_inventario=%s", (_id,))
    conexion.commit()

    return redirect('/admin/inventario')




# Perfil

@app.route('/admin/perfil')
def admin_perfil():

    if not 'login' in session:
        return redirect('/admin/login')

    return render_template('/admin/perfil.html')


# Contacto


@app.route('/admin/contacto')
def admin_contacto():

    if not 'login' in session:
        return redirect('/admin/login')

    return render_template('/admin/contacto.html')


if __name__ == '__main__':
    app.run(debug=True)