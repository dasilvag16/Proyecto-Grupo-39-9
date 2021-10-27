
import sqlite3
from sqlite3 import Error
conexion = ''
def get_db():
    try:
        conexion = sqlite3.connect("database/GestionEmpleados_DB.db")
        return conexion
    except Error:
        print(Error)

def close_db():
    conexion.close()


# def add_user():
#     nombre = request.form['nombre']
#     apellido = request.form['apellido']
#     cedula = request.form['cedula']
#     correo = request.form['correo']
#     telefono = request.form['telefono']
#     direccion = request.form['direccion']
#     celular = request.form['celular']
#     salario = request.form['salario']
#     dependencias = request.form['dependencias']
#     contrato = request.form['contrato']
#     usuario = request.form['usuario']
#     fechaingreso = request.form['fechaingreso']
#     password = request.form['password']
#     fechaterm = request.form['fechaterm']
#     cargo = request.form['cargo']
#     con = get_db()
#     cur = con.cursor(nombre, apellido, cedula, correo, telefono, direccion, celular,
#                      salario, dependencias, contrato, usuario, password, fechaingreso, fechaterm, cargo)
#     strsql = "INSERT INTO contacts (apellido, cedula, telefono, direccion, celular, salario, dependencias, contrato, fechaingreso, fechaterm,cargo) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
#         apellido, cedula, telefono, direccion, celular, salario, dependencias, contrato, fechaingreso, fechaterm, cargo)
#     strsql2 = "INSERT INTO Usuarios (nombre, usuario, correo, contrasena) VALUES ('{}','{}','{}','{}')".format(
#         nombre, usuario, correo, password)
#     cur.execute(strsql)
#     con.commit()
#     cur.execute(strsql2)
#     con.commit()
#     con.close()


def validateUserPass(usuario, contraseña):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE Usuario = '{}' and contraseña = '{}'".format(usuario, contraseña))
    registrosObtenidos = cur.fetchall()
    con.close()
    if registrosObtenidos:
        return True
    else:
        return False