# -------------------------------------------------------------------------------
# Programación para Web con Python y Flask
# Uso de SQLite
# -------------------------------------------------------------------------------

# Importamos librerías
from flask import Flask, render_template, request,jsonify,redirect

# Importamos SQLite
import sqlite3 as sql

#importamos conexcion con base datos
import db

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


