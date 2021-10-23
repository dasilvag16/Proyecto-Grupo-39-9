# -------------------------------------------------------------------------------
# Programación para Web con Python y Flask
# Uso de SQLite
# -------------------------------------------------------------------------------

# Importamos librerías
from flask import Flask, render_template, request,jsonify,redirect, url_for

# Importamos SQLite
import sqlite3 as sql



# Definimos la aplicación
app = Flask(__name__)

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
             empleados = 72
             cargos = 10
             establecidos = 150
             cumplidos = 145
             if usuario == 'admin':
                    return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
             elif usuario=='sadmin':
                    return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
             else:
                # deberia de enviarme a reigstrar
                return render_template('verinfo_us.html', user='Empleado')
        else:
                    return render_template('inicio_sesion.html')


@app.route('/definicion_listar', methods=['POST']) 
def definicion_listar():
    if usuario=='admin':
        return redirect ('/listar_admi')
    elif usuario=='sadmin':
        return redirect ('/listar_super')


@app.route('/editar_us', methods=['POST'])
def editar_us():
    return render_template('editar_us.html', user='Empleado')


@app.route('/ver_ret', methods=['POST'])
def ver_reto():
    return render_template('ver_ret.html', user='Empleado')


@app.route('/listar_admi')
def listar_admi():
    return render_template('listar_admi.html', user=usuario)


@app.route('/verinfo_admi', methods=['POST'])
def verinfo_admi():
    global temporal
    temporal = 'N/A'
    return render_template('verinfo_admi.html', user=usuario, temporal=temporal)


@app.route('/registrar_usuarios', methods=['POST'])
def registrar_usuarios():
    return render_template('registrar_usuarios.html', user=usuario)


@app.route('/editar_admi', methods=['POST'])
def editar_admi():
    return render_template('editar_admi.html', user=usuario, temporal=temporal)


@app.route('/eliminar', methods=['POST'])
def eliminar():
    return render_template('eliminar.html', user=usuario)


@app.route('/generar_ret', methods=['POST'])
def generar_ret():
    return render_template('generar_ret.html', user=usuario)


@app.route('/listar_super')
def listar_super():
    return render_template('listar_super.html', user=usuario)


@app.route('/asignar_roles')
def asignar_roles():
    return 'asignar roles'

