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


@app.route('/factura')
def factura():
    return render_template('sitio/factura.html')

@app.route('/factura_pasadia')
def factura_pasadia():
    return render_template('sitio/factura_pasadia.html')


@app.route('/alquiler')
def alquiler():
    return render_template('sitio/alquiler.html')

@app.route('/pasadia')
def pasadia():
    return render_template('sitio/pasadia.html')

@app.route('/eventos')
def eventos():
    return render_template('sitio/eventos.html')

@app.route('/reservaeventos')
def reservaeventos():
    return render_template('sitio/reservaeventos.html')

@app.route('/reservapasadia')
def reservapasadia():
    return render_template('sitio/reservapasadia.html')

@app.route('/reserva_exitosa')
def reserva_exitosa():
    return render_template('sitio/reserva_exitosa.html')


@app.route('/reserva_exitosa_pasadia')
def reserva_exitosa_pasadia():
    return render_template('sitio/reserva_exitosa_pasadia.html')




@app.route('/reservaeventos/guardar', methods=['POST'])
def reservaeventos_guardar():
    # Datos del cliente
    id_cliente = request.form['id_cliente']
    nombre_cliente = request.form['nombre_cliente']
    apellido_cliente = request.form['apellido_cliente']
    correo_cliente = request.form['correo_cliente']
    telefono_cliente = request.form['telefono_cliente']
    direccion_cliente = request.form['direccion_cliente']

    # Datos de la reserva
    cantidad = request.form['cantidad']
    fecha_ingreso = request.form['fecha_ingreso']
    fecha_salida = request.form['fecha_salida']

    # Calcular total (si lo manejas también en Python)
    # Si ya lo tienes en JS, puedes enviarlo en el formulario como input hidden
    total = request.form.get('total', 0)

    conexion = get_db()
    cursor = conexion.cursor()

    # Insertar cliente (solo si no existe)
    sql_cliente = """
        INSERT INTO cliente (id_cliente, nombre, apellido, correo_cliente, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            apellido = VALUES(apellido),
            correo_cliente = VALUES(correo_cliente),
            telefono = VALUES(telefono),
            direccion = VALUES(direccion)
    """
    datos_cliente = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, telefono_cliente, direccion_cliente)
    cursor.execute(sql_cliente, datos_cliente)

    try:
        # Insertar reserva (asociada al cliente)
        sql_reserva = """
            INSERT INTO reservas (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_ingreso, fecha_salida, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        datos_reserva = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_ingreso, fecha_salida, total)
        cursor.execute(sql_reserva, datos_reserva)

        conexion.commit()
        cursor.close()
        conexion.close()

        print(f"Cliente {nombre_cliente} {apellido_cliente} y su reserva han sido guardados correctamente.")
        return redirect('/reserva_exitosa')
    except Exception as e:
        print(f"Error al guardar la reserva: {str(e)}")
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        # En producción, usar flash() en lugar de print
        return "Error al procesar la reserva. Por favor, inténtelo de nuevo.", 500

    return redirect('/reserva_exitosa')

@app.route('/reservapasadia/guardar', methods=['POST'])
def guardar_reserva_pasadia():
    try:
        # === Datos del cliente ===
        id_cliente = request.form['id_cliente']
        nombre_cliente = request.form['nombre_cliente']
        apellido_cliente = request.form['apellido_cliente']
        correo_cliente = request.form['correo_cliente']
        telefono_cliente = request.form['telefono_cliente']
        direccion_cliente = request.form['direccion_cliente']

        # === Datos del pasadía ===
        fecha_pasadia = request.form['fecha_pasadia']
        cantidad = request.form['cantidad']
        tipo_pasadia = request.form['tipo_pasadia']
        total = request.form.get('total', 0)

        # === id_producto según tipo de pasadía ===
        if tipo_pasadia == "Publico":
            id_producto = 2
        elif tipo_pasadia == "Privado":
            id_producto = 3
        else:
            id_producto = None

        conexion = get_db()
        cursor = conexion.cursor()

        # === Guardar cliente (si no existe) ===
        sql_cliente = """
            INSERT INTO cliente (id_cliente, nombre, apellido, correo_cliente, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                nombre = VALUES(nombre),
                apellido = VALUES(apellido),
                correo_cliente = VALUES(correo_cliente),
                telefono = VALUES(telefono),
                direccion = VALUES(direccion)
        """
        datos_cliente = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, telefono_cliente, direccion_cliente)
        cursor.execute(sql_cliente, datos_cliente)

        # === Guardar reserva en reservas_pasadia ===
        sql_reserva = """
            INSERT INTO reservas_pasadia 
            (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_pasadia, id_producto, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        datos_reserva = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_pasadia, id_producto, total)
        cursor.execute(sql_reserva, datos_reserva)

        conexion.commit()
        cursor.close()
        conexion.close()

        print(f"✅ Reserva guardada: {nombre_cliente} {apellido_cliente} ({tipo_pasadia}) - Total: {total}")
        return redirect('/reserva_exitosa_pasadia')

    except Exception as e:
        print(f"❌ Error al guardar la reserva de pasadía: {str(e)}")
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and conexion:
            conexion.close()
        return "Error al procesar la reserva de pasadía", 500



@app.route('/contacto')
def contacto():
    return render_template('sitio/contacto.html')



@app.route('/contacto/guardar', methods=['POST'])
def contacto_guardar():

    nombre = request.form.get('nombre')
    correo_electronico = request.form.get('correo_electronico')
    mensaje = request.form.get('mensaje')

    # id_sugerencias assumed AUTO_INCREMENT - don't include it in the INSERT
    sql = "INSERT INTO `sugerencias` (`nombre`, `correo_electronico`, `mensaje`) VALUES (%s, %s, %s)"
    datos = (nombre, correo_electronico, mensaje)
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    cursor.close()
    conexion.close()
    
    print(nombre)
    print(correo_electronico)
    print(mensaje)
    
    return redirect('/contacto')

    
@app.route('/admin/')
def admin_index():

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
    correo_cliente = request.form['correo_cliente']
    telefono_cliente = request.form['telefono_cliente']
    direccion_cliente = request.form['direccion_cliente']

    sql = "INSERT INTO cliente (id_cliente, nombre, apellido, correo_cliente, telefono, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
    datos = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, telefono_cliente, direccion_cliente)
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_cliente)
    print(nombre_cliente)
    print(apellido_cliente)
    print(correo_cliente)
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

    cursor.execute("SELECT * FROM `casa`")
    casa = cursor.fetchall()
    conexion.commit()


    return render_template('admin/propietario.html', propietario=propietario, casa=casa)


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

    cursor.execute("SELECT * FROM `propietario`")
    propietarios = cursor.fetchall()
    conexion.commit()

    cursor.execute("SELECT * FROM `cliente`")
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/factura.html', factura=factura, productos=productos, propietarios=propietarios , clientes=clientes)


@app.route('/admin/factura/guardar', methods=['POST'])
def admin_factura_guardar():
    if not 'login' in session:
        return redirect('/admin/login')

    try:
        id_producto = request.form['id_producto']
        id_propietario = request.form['id_propietario']
        id_cliente = request.form['id_cliente']
        cantidad = request.form['cantidad']
        valor_venta = request.form['valor_venta']
        fecha_venta = request.form['fecha_venta']

        # La columna numero_factura se omite para usar AUTO_INCREMENT
        sql = """
            INSERT INTO `factura` 
            (`id_producto`, `id_propietario`, `id_cliente`, `cantidad`, `valor_venta`, `fecha_venta`) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        datos = (id_producto, id_propietario, id_cliente, cantidad, valor_venta, fecha_venta)
        
        conexion = get_db()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
        
        # Obtener el último ID insertado
        numero_factura = cursor.lastrowid
        
        print(f"Factura #{numero_factura} creada exitosamente")
        print(f"Producto: {id_producto}")
        print(f"Propietario: {id_propietario}")
        print(f"Cliente: {id_cliente}")
        print(f"Cantidad: {cantidad}")
        print(f"Valor: {valor_venta}")
        print(f"Fecha: {fecha_venta}")
        
        cursor.close()
        conexion.close()

    except Exception as e:
        print(f"Error al crear factura: {str(e)}")
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()
   

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

    cursor.execute("SELECT * FROM `tipo_producto`")
    tipo_producto = cursor.fetchall()
    conexion.commit()


    return render_template('admin/producto.html', producto=producto , tipo_producto=tipo_producto)


@app.route('/admin/producto/guardar', methods=['POST'])
def admin_producto_guardar():


    if not 'login' in session:
        return redirect('/admin/login')

    
    id_producto = request.form['id_producto']
    id_tipoproducto = request.form['id_tipoproducto']
    descripcion = request.form['descripcion']



    sql = "INSERT INTO `producto` (`id_producto`, `id_tipoproducto`, `descripcion`) VALUES (%s, %s, %s)"
    datos = (id_producto, id_tipoproducto, descripcion)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_producto)
    print(id_tipoproducto)
    print(descripcion)
   

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
    descripcion = request.form['descripcion']
    fecha_inventario = request.form['fecha_inventario']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']



    sql = "INSERT INTO `inventario` (`id_inventario`, `descripcion`, `fecha_inventario`, `cantidad`, `ubicacion`) VALUES (%s, %s, %s, %s, %s)"
    datos = (id_inventario, descripcion, fecha_inventario, cantidad, ubicacion)
    conexion = mysql.connector.connect(**config)
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_inventario)
    print(descripcion)
    print(fecha_inventario)
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

    
        
    return render_template('admin/perfil.html')


# Contacto


@app.route('/admin/contacto')
def admin_contacto():

    if not 'login' in session:
        return redirect('/admin/login')

    return render_template('/admin/contacto.html')


#reserva

@app.route('/admin/reservas')
def admin_reservas():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas`")
    reservas = cursor.fetchall()
    conexion.commit()
    print(reservas)

    cursor.execute("SELECT * FROM `producto`")
    productos = cursor.fetchall()
    conexion.commit()
    

    return render_template('admin/reservas.html', reservas=reservas, productos=productos)

@app.route('/admin/reservas/guardar', methods=['POST'])
def admin_reservas_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

    
    id_cliente = request.form['id_cliente']
    nombre_cliente = request.form['nombre_cliente']
    apellido_cliente = request.form['apellido_cliente']
    correo_cliente = request.form['correo_cliente']
    cantidad = request.form['cantidad']
    fecha_ingreso = request.form['fecha_ingreso']
    fecha_salida = request.form['fecha_salida']
    total = request.form['total']

    sql = "INSERT INTO reservas (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_ingreso, fecha_salida, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    datos = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_ingreso, fecha_salida, total)
    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    
    print(id_cliente)
    print(nombre_cliente)
    print(apellido_cliente)
    print(correo_cliente)
    print(cantidad)
    print(fecha_ingreso)
    print(fecha_salida)
    print(total)


    return redirect('/admin/reservas')

@app.route('/admin/reservas/borrar', methods=['POST'])
def admin_reservas_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    _id = request.form['txtID']
    print(_id)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas` WHERE id_reservas=%s", (_id,))
    reservas = cursor.fetchall()
    conexion.commit()
    print(reservas)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM reservas WHERE id_reservas=%s", (_id,))
    conexion.commit()

    return redirect('/admin/reservas')


#reserva_pasadia

@app.route('/admin/reservas_pasadia')
def admin_reservas_pasadias():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas_pasadia`")
    reservas_pasadia = cursor.fetchall()
    conexion.commit()
    print(reservas_pasadia)

    cursor.execute("SELECT * FROM `producto`")
    productos = cursor.fetchall()
    conexion.commit()
    

    return render_template('admin/reservas_pasadia.html', reservas_pasadia=reservas_pasadia, producto=productos)

@app.route('/admin/reservas_pasadia/guardar', methods=['POST'])
def admin_reservas_pasadia_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

    
    id_cliente = request.form['id_cliente']
    nombre_cliente = request.form['nombre_cliente']
    apellido_cliente = request.form['apellido_cliente']
    correo_cliente = request.form['correo_cliente']
    cantidad = request.form['cantidad']
    fecha_pasadia = request.form['fecha_pasadia']
    id_producto = request.form.get('id_producto')
    total = request.form['total']

    # Insertar incluyendo id_producto (viene del select en la plantilla)
    sql = "INSERT INTO reservas_pasadia (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_pasadia, id_producto, total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    datos = (id_cliente, nombre_cliente, apellido_cliente, correo_cliente, cantidad, fecha_pasadia, id_producto, total)

    conexion = None
    cursor = None
    try:
        conexion = get_db()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
    except Exception as e:
        print('Error guardando reserva pasadía:', str(e))
        if conexion:
            try:
                conexion.rollback()
            except Exception:
                pass
        # opcional: flash() para UX
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    print(id_cliente)
    print(nombre_cliente)
    print(apellido_cliente)
    print(correo_cliente)
    print(cantidad)
    print(fecha_pasadia)
    print(id_producto)
    print(total)


    return redirect('/admin/reservas_pasadia')

@app.route('/admin/reservas_pasadia/borrar', methods=['POST'])
def admin_reservas_pasadia_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    _id = request.form['txtID']
    print(_id)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas_pasadia` WHERE id_reservas_pasadia=%s", (_id,))
    reservas = cursor.fetchall()
    conexion.commit()
    print(reservas)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM reservas_pasadia WHERE id_reservas_pasadia=%s", (_id,))
    conexion.commit()

    return redirect('/admin/reservas_pasadia')



#reserva_eventos

@app.route('/admin/reservas_eventos')
def admin_reservas_eventos():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas_eventos`")
    reservas_eventos = cursor.fetchall()
    conexion.commit()
    print(reservas_eventos)

    cursor.execute("SELECT * FROM `producto`")
    productos = cursor.fetchall()
    conexion.commit()

    cursor.execute("SELECT * FROM `cliente`")
    cliente = cursor.fetchall()
    conexion.commit()
    

    return render_template('admin/reservas_eventos.html', reservas_eventos=reservas_eventos, producto=productos, cliente=cliente)

@app.route('/admin/reservas_eventos/guardar', methods=['POST'])
def admin_reservas_eventos_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

    
    id_cliente = request.form.get('id_cliente')
    cantidad_raw = request.form.get('cantidad')
    fecha_evento_raw = request.form.get('fecha_evento')
    id_producto_raw = request.form.get('id_producto')
    total_raw = request.form.get('total')

    # Validaciones y conversiones
    try:
        cantidad = int(cantidad_raw) if cantidad_raw not in (None, '') else None
    except ValueError:
        cantidad = None

    try:
        total = float(total_raw) if total_raw not in (None, '') else None
    except ValueError:
        total = None

    try:
        id_producto = int(id_producto_raw) if id_producto_raw not in (None, '') else None
    except ValueError:
        id_producto = None

    # Normalizar fecha a 'YYYY-MM-DD' si viene en ese formato
    try:
        if fecha_evento_raw:
            dt = datetime.strptime(fecha_evento_raw, '%Y-%m-%d')
            fecha_evento = dt.strftime('%Y-%m-%d')
        else:
            fecha_evento = None
    except Exception:
        fecha_evento = fecha_evento_raw

    # Corregir nombre de columna: usar 'fecha_evento' (singular) para coincidir con el form
    sql = "INSERT INTO reservas_eventos (id_cliente, cantidad, fecha_evento, id_producto, total) VALUES (%s, %s, %s, %s, %s)"
    datos = (id_cliente, cantidad, fecha_evento, id_producto, total)

    # Log de la tupla a insertar
    print('-> Datos a insertar en reservas_eventos:', datos)

    conexion = None
    cursor = None
    try:
        conexion = get_db()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
    except Exception as e:
        print('Error guardando reserva eventos:', str(e))
        if conexion:
            try:
                conexion.rollback()
            except Exception:
                pass
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

    print('id_cliente=', id_cliente)
    print('cantidad=', cantidad)
    print('fecha_evento=', fecha_evento)
    print('id_producto=', id_producto)
    print('total=', total)


    return redirect('/admin/reservas_eventos')

@app.route('/admin/reservas_eventos/borrar', methods=['POST'])
def admin_reservas_eventos_borrar():


    if not 'login' in session:
        return redirect('/admin/login')
    
    _id = request.form['txtID']
    print(_id)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `reservas_eventos` WHERE id_reservas_eventos=%s", (_id,))
    reservas = cursor.fetchall()
    conexion.commit()
    print(reservas)

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM reservas_eventos WHERE id_reservas_eventos=%s", (_id,))
    conexion.commit()

    return redirect('/admin/reservas_eventos')



# Sugerencias

@app.route('/admin/sugerencias')
def admin_sugerencias():

    if not 'login' in session:
        return redirect('/admin/login')

    conexion = get_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `sugerencias`")
    sugerencias = cursor.fetchall()
    conexion.commit()
    print(sugerencias)


    return render_template('admin/sugerencias.html', sugerencias=sugerencias)


# Calendario citas
# 🗓 Ruta para mostrar el calendario
@app.route('/admin/calendario')
def calendario():
    return render_template('admin/calendario.html')

# 📅 Ruta que devuelve los datos JSON de las reservas
@app.route('/eventos_data')
def eventos_data():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        eventos = []

        # Consulta para reservas de alojamiento (azul)
        cursor.execute("""
            SELECT 
                CONCAT('R', id_reservas) as id,
                CONCAT(nombre_cliente, ' - Alojamiento') as title,
                fecha_ingreso as start,
                fecha_salida as end,
                '#0072ff' as color,
                total
            FROM reservas
        """)
        eventos.extend(cursor.fetchall())

        # Consulta para reservas de pasadía (verde)
        cursor.execute("""
            SELECT 
                CONCAT('P', id_reservas_pasadia) as id,
                CONCAT(nombre_cliente, ' - Pasadía') as title,
                fecha_pasadia as start,
                fecha_pasadia as end,
                '#00c853' as color,
                total
            FROM reservas_pasadia
        """)
        eventos.extend(cursor.fetchall())

        # Consulta para reservas de eventos (naranja)
        cursor.execute("""
            SELECT 
                CONCAT('E', id_reservas_eventos) as id,
                CONCAT('Evento: ', id_cliente) as title,
                fecha_evento as start,
                fecha_evento as end,
                '#ff9800' as color,
                total
            FROM reservas_eventos
        """)
        eventos.extend(cursor.fetchall())

        # Formatear las fechas y validar datos
        for evento in eventos:
            if evento['start']:
                evento['start'] = str(evento['start'])
            if evento['end']:
                evento['end'] = str(evento['end'])
            else:
                evento['end'] = evento['start']

            evento['title'] = evento['title'] or 'Reserva sin nombre'
            
            # Para eventos de un día, marcarlos como allDay
            if evento['start'] == evento['end']:
                evento['allDay'] = True

        cursor.close()
        conn.close()
        return jsonify(eventos)

    except Exception as e:
        print(f"Error al obtener eventos: {str(e)}")
        return jsonify([])  # Devolver lista vacía en caso de error

if __name__ == '__main__':
    app.run(debug=True)