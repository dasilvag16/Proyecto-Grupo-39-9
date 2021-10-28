# -------------------------------------------------------------------------------
# Programación para Web con Python y Flask
# Uso de SQLite
# -------------------------------------------------------------------------------

# Importamos librerías
from flask import Flask, render_template, request,jsonify,redirect, url_for, flash, session

# Importamos SQLite
import sqlite3 as sql
import db
from sqlite3 import Error


# Definimos la aplicación
app = Flask(__name__)
# Se define llave secreta
app.secret_key = 'mi_llave secreta'

#se define la ruta inicial
@app.route('/')
def home():
    return render_template('inicio_sesion.html')


#Funcion para validar usuario
def validateUserPass(usuario,contraseña):
    
    # Se conecta a la Base de Datos
    con = sql.connect("gestionempleados.db")
    con.row_factory = sql.Row

    # Crea un cursor
    cur = con.cursor()

    # Ejecuta consultas
    cur.execute("SELECT * FROM Usuarios WHERE Usuario = '{}' and contraseña = '{}'".format(usuario, contraseña))

    # Obtiene los recursos
    registrosObtenidos = cur.fetchall()

    # Renderiza listar.html
    #return render_template("listar.html", rows=registrosObtenidos)
            
    if registrosObtenidos:
            return True
    else:
            return False


    
#definir ruta para login
@app.route('/login',methods=['POST'])
#funcion de validacion
def validar():
    #verifica que sea POST
    if request.method == 'POST':
        global usuario

        #obteniendo datos
        usuario=request.form['usuario']
        password=request.form['contraseña']
        

        #llamando funcion de conexion base de datos con parametros de variables creadas
        if validateUserPass(usuario,password):
             #Se crea el vector para la sesión
             session['usuario'] = usuario
             empleados = 72
             cargos = 10
             establecidos = 150
             cumplidos = 145
             if usuario == 'admin':
                    return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
             elif usuario=='sadmin':
                    return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
             else:
                # Se consulta las tablas Usuarios y Empleados y se obtienen los registros
                cone = sql.connect("database/GestionEmpleados_DB.db")
                cursor = cone.cursor()
                cursor.execute("SELECT * FROM Usuarios WHERE Usuario = '{}'".format(usuario))
                registrosObtenidos = cursor.fetchone()
                cursor.execute("select * from Empleados WHERE idEmpleados = {}".format(registrosObtenidos[0]))
                registro = cursor.fetchone()
                #Se crean variables globales para ahorrarse un futura consulta
                global nombre, apellido, cedula, correo, celular, fijo, direccion, salario, ingreso, terminacion, cargo, dependencia, contrato
                #Se asignan los registros de las tablas a variables
                nombre = registrosObtenidos[1]
                apellido = registro[11]
                cedula = registrosObtenidos[0]
                correo = registrosObtenidos[3]
                celular = registro[1]
                fijo = registro[2]
                direccion = registro[3]
                salario = registro[4]
                ingreso = registro[5]
                terminacion = registro[6]
                cargo = registro[7]
                dependencia = registro[9]
                contrato = registro[10]
                cone.close()
                return render_template('verinfo_us.html', user=usuario, cel=celular, fijo=fijo, direccion=direccion, salario=salario,
                ingreso=ingreso, terminacion=terminacion, cargos=cargo, dependencia=dependencia, contrato=contrato,
                nombre=nombre, apellido=apellido, cedula=cedula, correo=correo)
        else:
                return render_template('inicio_sesion.html')


@app.route('/definicion_listar', methods=['POST']) 
def definicion_listar():
    if usuario=='admin':
        return redirect ('/listar_admi')
    elif usuario=='sadmin':
        return redirect ('/listar_super')


@app.route('/editar_us/', methods=['POST', 'GET'])
def editar_us():
    #Si se viene desde la ruta /login se ejecuta la sentencia if
    if request.method == 'GET':    
        return render_template('editar_us.html', user=usuario, cel=celular, fijo=fijo, direccion=direccion, 
        salario=salario, ingreso=ingreso, terminacion=terminacion, cargos=cargo, dependencia=dependencia,
        contrato=contrato, nombre=nombre, apellido=apellido, cedula=cedula, correo=correo)
    #Si se actualiza los datos se ejecuta la sentencia else
    else:
        return update_editar_us()

#Función para actualizar los registros de las tablas
def update_editar_us():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    fijo = request.form['telefono']
    direccion = request.form['direccion']
    celular = request.form['celular']
    cone = sql.connect("database/GestionEmpleados_DB.db")
    cursor = cone.cursor()
    cursor.execute("UPDATE Empleados SET Celular='"+str(celular)+"', Fijo='"+str(fijo)+"', Direccion='"+direccion+"', Apellidos='"+apellido+"' WHERE idEmpleados = '"+str(cedula)+"'")    
    cursor.execute("UPDATE Usuarios SET Nombres='"+nombre+"', Correo='"+correo+"' WHERE idUsuarios = '"+str(cedula)+"'")
    cone.commit()
    cone.close()
    return render_template('editar_us.html', user=usuario, cel=celular, fijo=fijo, direccion=direccion, 
        salario=salario, ingreso=ingreso, terminacion=terminacion, cargos=cargo, dependencia=dependencia,
        contrato=contrato, nombre=nombre, apellido=apellido, cedula=cedula, correo=correo)

@app.route('/ver_ret', methods=['POST'])
def ver_reto():
    #Se consulta la tabla Retroalimentacion y se trae la información
    cone = sql.connect("database/GestionEmpleados_DB.db")
    cursor = cone.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE Usuario = '{}'".format(usuario))
    registrosObtenidos = cursor.fetchone()
    cursor.execute("select * from Retroalimentacion WHERE idRetroalimentacion = {}".format(registrosObtenidos[0]))
    registro = cursor.fetchone()
    desempeño = registro[1]
    puntaje = registro[2]
    nya = nombre+' '+apellido
    cone.close()
    return render_template('ver_ret.html', user=usuario, desempeño=desempeño, puntaje=puntaje, nya=nya, 
    cedula=cedula, dependencia=dependencia, ingreso=ingreso)


@app.route('/listar_admi', methods=['POST', 'GET'])
def listar_admi():
    if request.method == 'GET':
        #print(request.url)
        return render_template('listar_admi.html', user=usuario)
    else:
        return buscar_admi()

def buscar_admi():
    try:
        busqueda = request.form['BuscarUsuario']
        con = db.get_db()
        cur = con.cursor()
        strsql = "SELECT * FROM Empleados WHERE idEmpleados = {}".format(busqueda)
        strsql1 = "SELECT * FROM Usuarios WHERE idUsuarios = {}".format(busqueda)
        cur.execute(strsql)
        datos = cur.fetchone()
        cur.execute(strsql1)
        datos1 = cur.fetchone()
        nya = datos1[1]+' '+datos[11]
        cedula = datos1[0]
        con.close()
        return render_template('listar_admi.html', user=usuario, nya=nya, cedula=cedula)
    except TypeError:
        return render_template('listar_admi.html', user=usuario)
    except Error:
        return render_template('listar_admi.html', user=usuario)

# @app.route('/verinfo_admi', methods=['POST'])
# def verinfo_admi():
#     con = db.get_db()
#     cur = con.cursor()
#     strsql = "SELECT * FROM Empleados WHERE idEmpleados = {}".format(1)
#     strsql1 = "SELECT * FROM Usuarios WHERE idUsuarios = {}".format(1)
#     strsql2 = "SELECT * FROM Retroalimentacion WHERE idRetroalimentacion = {}".format(1)
#     cur.execute(strsql)
#     datos = cur.fetchone()
#     cur.execute(strsql1)
#     datos1 = cur.fetchone()
#     cur.execute(strsql2)
#     datos2 = cur.fetchone()
#     cedula = datos[0]
#     celular = datos[1]
#     fijo = datos[2]
#     direccion = datos[3]
#     salario = datos[4]
#     ingreso = datos[5]
#     term = datos[6]
#     cargo = datos[7]
#     dependencias = datos[9]
#     contrato = datos[10]
#     apellido = datos[11]
#     nombre = datos1[1]
#     usuario1 = datos1[2]
#     correo = datos1[3]
#     contraseña = datos1[4]
#     retroalimentacion = datos2[1]
#     return render_template('verinfo_admi.html', user=usuario, cedula=cedula, celular=celular, fijo=fijo, direccion=direccion,
#         salario=salario, ingreso=ingreso, term=term, cargo=cargo, dependencias=dependencias, contrato=contrato,
#         apellido=apellido, nombre=nombre, usuario1=usuario1, correo=correo, contraseña=contraseña, retroalimentacion=retroalimentacion)


@app.route('/registrar_usuarios', methods=['POST', 'GET'])
def registrar_usuarios():   
    if request.method == 'GET':    
        return render_template('registrar_usuarios.html', user=usuario)
    #Si se actualiza los datos se ejecuta la sentencia else
    else:
        return add_user() 
        #return render_template('registrar_usuarios.html', user=usuario)

def add_user():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    correo = request.form['correo']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    celular = request.form['celular']
    salario = request.form['salario']
    dependencias = request.form['dependencias']
    contrato = request.form['contrato']
    usuario_r = request.form['usuario_r']
    fechaingreso = request.form['fechaingreso']
    password = request.form['password_r']
    fechaterm = request.form['fechaterm']
    cargo = request.form['cargo']
    rol = False
    ###### OJO ########
    con = sql.connect("database/GestionEmpleados_DB.db")
    ###################
    cur = con.cursor()
    strsql = "INSERT INTO Empleados (idEmpleados, Celular, Fijo, Direccion, Salario, Fecha_ingreso, Fecha_terminacion, Cargo, Rol, Dependencia, Tipo_contrato, Apellidos) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        cedula, celular, telefono, direccion, salario, fechaingreso, fechaterm, cargo, rol, dependencias, contrato, apellido)
    strsql2 = "INSERT INTO Usuarios (idUsuarios, Nombres, Usuario, Correo, Contraseña) VALUES ('{}','{}','{}','{}','{}')".format(
        cedula, nombre, usuario_r, correo, password)
    cur.execute(strsql)
    con.commit()
    cur.execute(strsql2)
    con.commit()
    con.close()
    return render_template('registrar_usuarios.html', user=usuario)


@app.route('/editar_admi', methods=['POST', 'GET'])
def editar_admi():
    if request.method == 'GET':
        return render_template('editar_admi.html', user=usuario)
    else:
        return fill()
    
def fill():
    try:
        global busqueda1
        busqueda1 = request.form['BuscarUsuario']
        con = db.get_db()
        cur = con.cursor()
        strsql = "SELECT * FROM Empleados WHERE idEmpleados = {}".format(busqueda1)
        strsql1 = "SELECT * FROM Usuarios WHERE idUsuarios = {}".format(busqueda1)
        strsql2 = "SELECT * FROM Retroalimentacion WHERE idRetroalimentacion = {}".format(busqueda1)
        cur.execute(strsql)
        datos = cur.fetchone()
        cur.execute(strsql1)
        datos1 = cur.fetchone()
        cur.execute(strsql2)
        datos2 = cur.fetchone()
        cedula = datos[0]
        celular = datos[1]
        fijo = datos[2]
        direccion = datos[3]
        salario = datos[4]
        ingreso = datos[5]
        term = datos[6]
        cargo = datos[7]
        dependencias = datos[9]
        contrato = datos[10]
        apellido = datos[11]
        nombre = datos1[1]
        usuario1 = datos1[2]
        correo = datos1[3]
        contraseña = datos1[4]
        reseña = datos2[1]
        puntaje = datos2[2]
        return render_template('editar_admi.html', user=usuario, cedula=cedula, celular=celular, fijo=fijo, direccion=direccion,
            salario=salario, ingreso=ingreso, term=term, cargo=cargo, dependencias=dependencias, contrato=contrato,
            apellido=apellido, nombre=nombre, usuario1=usuario1, correo=correo, contraseña=contraseña, reseña=reseña, puntaje=puntaje)
    except TypeError:
        return render_template('editar_admi.html', user=usuario)
    except Error:
        return render_template('editar_admi.html', user=usuario)

@app.route('/editar', methods=['POST'])
def editar():
    nombre = request.form['nombres']
    identificacion = request.form['identificacion']
    fijo = request.form['fijo']
    celular = request.form['celular']
    dependencias = request.form.get('dependencias')
    ingreso = request.form['ingreso']
    terminacion = request.form['terminacion']
    contrato = request.form.get('contrato')
    cargo = request.form['cargo']
    apellidos = request.form['apellidos']
    correo = request.form['correo']
    direccion = request.form['direccion']
    salario = request.form['salario']
    usuario2 = request.form['usuario2']
    contraseña = request.form['contraseña']
    reseña = request.form['reseña']
    puntaje = request.form['puntaje']
    con = db.get_db()
    cur = con.cursor()
    cur.execute("SELECT Rol FROM Empleados WHERE idEmpleados = '{}'".format(busqueda1))
    rolex = cur.fetchone()
    rol = rolex[0]
    strsql = "UPDATE Empleados SET idEmpleados='"+str(identificacion)+"', Celular='"+str(celular)+"', Fijo='"+str(fijo)+"', Direccion='"+direccion+"', Salario='"+salario+"', Fecha_ingreso='"+ingreso+"', Fecha_terminacion='"+terminacion+"', Cargo='"+cargo+"', Rol='"+str(rol)+"', Dependencia='"+dependencias+"', Tipo_contrato='"+contrato+"', Apellidos='"+apellidos+"' WHERE idEmpleados = '"+str(busqueda1)+"'"
    strsql1 = "UPDATE Usuarios SET idUsuarios='"+str(identificacion)+"', Nombres='"+nombre+"', Usuario='"+usuario2+"', Correo='"+correo+"', Contraseña='"+contraseña+"' WHERE idUsuarios = '"+str(busqueda1)+"'"
    strsql2 = "UPDATE Retroalimentacion SET idRetroalimentacion='"+str(identificacion)+"', Reseña='"+reseña+"', Puntaje='"+str(puntaje)+"' WHERE idRetroalimentacion='"+str(busqueda1)+"'"
    cur.execute(strsql)
    cur.execute(strsql1)
    cur.execute(strsql2)
    con.commit()
    con.close()
    return redirect('/editar_admi')

@app.route('/eliminar', methods=['POST', 'GET'])
def eliminar():
    if request.method == 'GET':
        return render_template('eliminar.html', user=usuario)
    else:
        return buscar_eliminar()

def buscar_eliminar():
    try:
        global busqueda2
        busqueda2 = request.form['BuscarUsuario']
        con = db.get_db()
        cur = con.cursor()
        strsql = "SELECT * FROM Empleados WHERE idEmpleados = {}".format(busqueda2)
        strsql1 = "SELECT * FROM Usuarios WHERE idUsuarios = {}".format(busqueda2)
        cur.execute(strsql)
        datos = cur.fetchone()
        cur.execute(strsql1)
        datos1 = cur.fetchone()
        nya = datos1[1]+' '+datos[11]
        cedula = datos1[0]
        con.close()
        return render_template('eliminar.html', user=usuario, nya=nya, cedula=cedula)
    except TypeError:
        return render_template('eliminar.html', user=usuario)
    except Error:
        return render_template('eliminar.html', user=usuario)

@app.route('/eliminar_user', methods=['POST'])
def eliminar_user():
    con = db.get_db()
    cur = con.cursor()
    strsql = "delete from Empleados where idEmpleados = '"+str(busqueda2)+"';"
    strsql1 = "delete from Usuarios where idUsuarios = '"+str(busqueda2)+"';"
    strsql2 = "delete from Retroalimentacion where idRetroalimentacion = '"+str(busqueda2)+"';"
    cur.execute(strsql)
    cur.execute(strsql1)
    cur.execute(strsql2)
    con.commit()
    con.close()
    return redirect('/eliminar')
# @app.route('/generar_ret', methods=['POST'])
# def generar_ret():
#     return render_template('generar_ret.html', user=usuario)


@app.route('/listar_super', methods=['POST', 'GET'])
def listar_super():
    if request.method == 'GET':
        return render_template('listar_super.html', user=usuario)
    else:
        return buscar_admi1()

def buscar_admi1():
    try:
        busqueda = request.form['BuscarUsuario']
        con = db.get_db()
        cur = con.cursor()
        strsql = "SELECT * FROM Empleados WHERE idEmpleados = {}".format(busqueda)
        strsql1 = "SELECT * FROM Usuarios WHERE idUsuarios = {}".format(busqueda)
        cur.execute(strsql)
        datos = cur.fetchone()
        cur.execute(strsql1)
        datos1 = cur.fetchone()
        nya = datos1[1]+' '+datos[11]
        cedula = datos1[0]
        rol1 = request.form.get('Roles')
        if rol1 == 'Administrador':
            roles1 = True
            cur.execute("UPDATE Empleados SET Rol='"+str(roles1)+"' WHERE idEmpleados = "+str(cedula)+"")
            con.commit()
            con.close()
            return render_template('listar_super.html', user=usuario, nya=nya, cedula=cedula)
        elif rol1 == 'gerencia':
            roles1 = False
            cur.execute("UPDATE Empleados SET Rol='"+str(roles1)+"' WHERE idEmpleados = "+str(cedula)+"")
            con.commit()
            con.close()
            return render_template('listar_super.html', user=usuario, nya=nya, cedula=cedula)
        else:
            con.close()
            return render_template('listar_super.html', user=usuario, nya=nya, cedula=cedula)
    except TypeError:
        return render_template('listar_super.html', user=usuario)
    except Error:
        return render_template('listar_super.html', user=usuario)

#Ruta para la creación de sesiones
@app.before_request
def antes_peticion():
    if 'usuario' not in session and request.endpoint in ['editar_us']:
        return redirect('/')
    if 'usuario' not in session and request.endpoint in ['registrar_usuarios']:
        return redirect('/')
    if 'usuario' not in session and request.endpoint in ['listar_super']:
        return redirect('/')
    if 'usuario' not in session and request.endpoint in ['listar_admi']:
        return redirect('/')

#Ruta para cerrar sesiones
@app.route('/cerrar_sesion')
def cerrar_sesion():
    if 'usuario' in session:
        session.pop('usuario')
    
    return redirect('/')
