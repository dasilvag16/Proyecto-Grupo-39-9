from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('inicio_sesion.html')


@app.route('/validar_usuario', methods=['POST'])
def validar_usuario():
    global usuario
    usuario = request.form["usuario"]
    empleados = 72
    cargos = 10
    establecidos = 150
    cumplidos = 145
    if usuario == 'Superadministrador':
        return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
    elif usuario=='Administrador':
        return render_template('dashboard.html', user=usuario, empleados=empleados, cargos=cargos, establecidos=establecidos, cumplidos=cumplidos)
    else:
        # deberia de enviarme a reigstrar
        return render_template('verinfo_us.html', user='Empleado')


@app.route('/definicion_listar', methods=['POST'])  # Error de metodo
def definicion_listar():
    if usuario=='Administrador':
        return redirect ('/listar_admi')
    elif usuario=='Superadministrador':
        return redirect ('/listar_super')
        
# def enviar_usuario_nuevo():
#     return redirect('/registrar_usuarios')

# def enviar_verinfo():
#     return redirect('/verinfo_admi')

# def enviar_editar():
#     return redirect('/editar_admi')

# def enviar_eliminar():
#     return redirect('/eliminar')

# def enviar_generar_ret():
#     return redirect('/generar_ret')

# def enviar_editar_us():
#     return redirect('/editar_us')

# def enviar_ver_ret():
#     return redirect('/ver_ret')

#Borrado temporalmente debido a pruebas


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
