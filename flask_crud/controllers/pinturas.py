from flask import redirect, render_template, request, flash, session
from flask_crud import app
from flask_crud.models.pintura import Pintura
from flask_crud.models.usuario import Usuario



@app.route("/panel")
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')
    
    return render_template("panel.html",  pinturas=Pintura.get_all_pinturas())

@app.route("/pintura/<int:id>")
def pintura_id(id):
    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/') 
        
    return render_template("pintura.html",  pinturas=Pintura.get_by_id2(id))


@app.route("/pintura/nueva")
def nueva_pintura():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/')

    return render_template("nueva_pintura.html")
    


@app.route("/procesar_pintura/", methods=["POST"])
def procesar_pintura():

    if not Pintura.validar_pintura(request.form):
        return redirect('/panel')

    data = {
        'titulo' : request.form['titulo'],
        'descripcion' : request.form['descripcion'],
        'precio' : request.form['precio'],
        'usuario_creador': session['usuario_creador'],

    }

    resultado = Pintura.save_pintura(data)
    print(resultado)
    

    if not resultado:
        flash("error al crear la pintura", "error")
        return redirect("/panel")

    flash("pintura creado correctamente", "success")
    return redirect("/panel")

@app.route("/pintura/<id>/editar")
def editar(id):
    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/')

    pintura=Pintura.get_by_id3(id)
    return render_template('edit.html',pintura=pintura[0])
    

@app.route("/procesar_actualizacion/<int:id>", methods=["POST"])
def Actualizar_pintura(id):
    print(Actualizar_pintura)
    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/')
    
    if not Pintura.validar_pintura(request.form):
        return redirect('/panel')
    
    actz_pintura= {
            "id":id,
            'titulo':request.form['titulo'],
            'descripcion':request.form['descripcion'],
            'precio':request.form['precio'],
            'usuario_creador': session["usuario_creador"]

        }

    resultado= Pintura.update_pintura(actz_pintura)

    if not resultado:
            flash("error al crear el usuario", "error")
            return redirect("/panel")

    flash("Usuario creado correctamente", "success")
    return redirect("/panel")







@app.route("/eliminar/pintura/<id>", methods=['GET', 'POST'])
def delete1(id):
    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/')
    
    data= {
        'id': id
    }

    Pintura.delete(data)
    flash("pintura  eliminado", "success")
    return redirect("/panel")