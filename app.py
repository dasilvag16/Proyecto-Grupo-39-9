from flask import Flask, render_template, request, redirect

app = Flask(__name__)
@app.route('/') 
def inicio():
    return render_template('inicio_sesion.html')

@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    usuario = request.form["usuario"]
    if usuario=='Superadministrador':
        return render_template('dashboard.html', user=usuario)
    elif usuario=='Administrador':
        return render_template('dashboard.html', user=usuario)
    else:
        return render_template('verinfo_us.html', user='Empleado')

@app.route('/probando')
def probando():
    return render_template('layout1.html')

@app.route('/editar_us') 
def editar_us():
    return 'editar usuario propio'

@app.route('/ver_ret') 
def ver_reto():
    return 'ver retroalimentación'

@app.route('/listar_admi') 
def listar_admi():
    return 'listar usuarios administrador'

@app.route('/verinfo_admi') 
def verinfo_admi():
    return 'ver información administrador y superadministrador'

@app.route('/registrar_usuarios') 
def registrar_usuarios():
    return 'registrar usuarios administrador y superadministrador'

@app.route('/editar_admi') 
def editar_admi():
    return 'editar administrador y superadministrador'

@app.route('/eliminar') 
def eliminar():
    return 'eliminar administrador y superadministrador'

@app.route('/generar_ret') 
def generar_ret():
    return 'generar retroalimentacion administrador y superadministrador'

@app.route('/listar_super') 
def listar_super():
    return 'listar usuarios superadministrador'

@app.route('/asignar_roles') 
def asignar_roles():
    return 'asignar roles'