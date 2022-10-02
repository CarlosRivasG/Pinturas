from flask import redirect, render_template, request, flash, session
from flask_crud import app
from flask_crud.models.pintura import Pintura
from flask_crud.models.usuario import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    if not Usuario.validar(request.form):
        return redirect('/')

    pass_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/")

    flash("Usuario creado correctamente", "success")
    return redirect("/")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identificacion'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/")

    session['usuario'] = usuario.nombre
    session['usuario_creador'] = usuario.id
    session['apellido'] = usuario.apellido

    return redirect('/panel')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')