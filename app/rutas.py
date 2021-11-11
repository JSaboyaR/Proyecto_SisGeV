from wtforms import form
from main import app
from flask import render_template, redirect, request
from flask import Flask, render_template, redirect, session, flash, request, send_file
from flask.helpers import make_response, url_for
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from dataBase import elegirlist, validardata, listadata, eliminardata
from datetime import datetime


from app.forms import FormLogin
from app.forms import FormRegistro
from app.forms import FormBuscarV
from app.forms import FormReservar 
from app.forms import FormCalificar
from app.forms import FormAgregarV
from app.forms import FormEliminarV
from app.forms import FormEditarV
from app.forms import FormComentar
from app.forms import FormRegistroAdmin
from app.forms import listapilotos



@app.route('/', methods=['POST', 'GET'])
def login():
    forms = FormLogin()
    if request.method == "GET":
        return render_template('login.html', form = forms)
    if request.method =="POST":
        nombre = escape(forms.usuario.data.strip())
        password = escape(forms.contrasena.data.strip())
        database = "SELECT nombre, cedula, correo, telefono, contraseña, tipo FROM usuarios WHERE usuario=?"
        lista = listadata(database, nombre)
        if len(lista)==0:
            flash('*El usuario no existe')
            return render_template('login.html', form = forms)
        else:
            clave = lista[0][4]
        if check_password_hash(clave, password):
            session.clear()
            session['name'] = lista[0][0]
            session['user'] = nombre
            session['id'] = lista[0][1]
            session['email'] = lista[0][2]
            session['phone'] = lista[0][3]
            session['type'] = lista[0][5]
            fecha= datetime.today().strftime('%Y-%m-%d')
            database = "INSERT INTO controles(usuario, fecha) VALUEs (?,?);"
            validar = validardata(database,(nombre,fecha))
            if validar!=0:
                print('Datos almacenados con éxito')
            else:
                print('*Error')
            return redirect('/home')
        else:
            flash('*Usuario o clave invalidas')
            return render_template('login.html', form = forms)
        

@app.route('/logout')
def logout():
    session.clear()
    flash('La sesión ha cerrado')
    return redirect('/')


@app.route('/registro', methods=['POST', 'GET'])
def registro():
    e1, e2, e3, e4, e5, e6, e7 = " ", " ", " ", " ", " ", " ", " "
    forms = FormRegistro()
    if request.method == "GET":
        return render_template('registro.html', form = forms)
    else:
        nombre1 = escape(request.form['nombre'])
        cedula1 = escape(request.form['cedula'])
        correo1 = escape(request.form['correo'])
        telefono1 = escape(request.form['telefono'])
        usuario1 = escape(request.form['usuario'])
        contrasena1 = escape(request.form['contrasena'])
        aceptar1 = escape(request.form.get('aceptar'))
        tipo = 3
    
        verror = False

        if nombre1==None or len(nombre1)==0:
            verror = True
            e1 = "- nombre -"
        if cedula1==None or len(cedula1)==0:
            verror = True
            e2 = "- cédula -"
        if correo1==None or len(correo1)==0:
            verror = True
            e3 = "- correo -"
        if telefono1==None or len(telefono1)==0:
            verror = True
            e4 = "- teléfono -"
        if usuario1==None or len(usuario1)==0:
            verror = True
            e5 = "- usuario ej:aA123456 -"
        if contrasena1==None or len(contrasena1)==0:
            verror = True
            e6 = "- contraseña ej:aA123456 -"
        if aceptar1==None or aceptar1=='None':
            verror = True
            e7 = "- aceptar condiciones -"
        if (verror):
            flash('*Validar: {}{}{}{}{}{}{}'.format(e1,e2,e3,e4,e5,e6,e7))

        if not verror:
            database = "INSERT INTO USUARIOS(nombre, cedula, correo, telefono, usuario, contraseña, tipo, aceptar) VALUEs (?, ?, ?, ?, ?, ?, ?, ?)"
            password = generate_password_hash(contrasena1)
            validar = validardata(database,(nombre1, cedula1, correo1, telefono1, usuario1, password, tipo, aceptar1))
            if validar!=0:
                flash('Datos almacenados con éxito')
            else:
                flash('*El usuario ya existe, intente con otro')
        return render_template('registro.html', form = forms)

@app.route('/home')
def home():
    try:
        tipo = session['type']   
        return render_template('home.html', titulo = 'Home', tipo=tipo)
    except:
        return render_template('error.html')


@app.route('/home/dashboard')
def dashboard():
    try:
        tipo = session['type']
        database = "SELECT usuario from controles"
        total1 = elegirlist(database)
        totaling = len(total1)

        database1 = "SELECT codigo from vuelos"
        total2 = elegirlist(database1)
        totalvuelos = len(total2)

        database2 = "SELECT nombre from usuarios"
        total2 = elegirlist(database2)
        totalusuarios = len(total2)

        database3 = "SELECT codigo from reservas"
        total3 = elegirlist(database3)
        totalreservas = len(total3)

        database4 = "SELECT id from comentarios"
        total4 = elegirlist(database4)
        totalcomentarios = len(total4)
    

        registros = [totaling, totalvuelos, totalusuarios, totalreservas, totalcomentarios]
        return render_template('dashboard.html', titulo = 'Dashboard', registros = registros, tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/usuario')
def usuario():
    try:
        tipo = session['type']
        return render_template('Usuario.html', titulo = 'Usuario', tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/usuarioLbuscarv', methods=['POST', 'GET'])
def buscarv():
    try:
        forms = FormBuscarV()
        tipo = session['type']
        if request.method == "GET":
            return render_template('buscarVuelo.html', form = forms, titulo = 'Busqueda', tipo=tipo)
        else:
            codigo1 = escape(request.form['codigoB'])
            database = "SELECT codigo, avion, origen, destino, piloto, capacidad, estado FROM vuelos WHERE codigo=?"
            lista = listadata(database, codigo1)
            if len(lista)==0:
                flash('*El vuelo no está registrado')
                return render_template('buscarVuelo.html', form = forms, titulo = 'Busqueda', tipo=tipo)
            elif len(lista)!=0:
                flash('El vuelo encontrado')
                return render_template('buscarVuelo.html', form = forms, titulo = 'Busqueda', vuelo = lista, tipo=tipo)
    except:
        return render_template('error.html')
            

@app.route('/home/usuarioLreservarv', methods=['POST', 'GET'])
def reservarv():
    try:
        forms = FormReservar()
        habilitar = 1
        tipo = session['type']
        if request.method == "GET":
            return render_template('reservarVuelo.html', form = forms, titulo = 'Reserva', habilitar = habilitar, tipo=tipo)
        if request.method =="POST":
            if request.form.get('buscar') == 'Buscar':
                origen1 = escape(request.form['origen'])
                destino1 = escape(request.form['destino'])
                database = "SELECT codigo, avion, origen, destino, piloto, capacidad, estado FROM vuelos WHERE origen=?"
                lista = listadata(database, origen1)
                if len(lista)==0:
                    flash('*Vuelos no disponibles')
                    return render_template('reservarVuelo.html', form = forms, titulo = 'Reserva', destino = destino1, habilitar = habilitar, tipo=tipo)
                elif len(lista)!=0:
                    habilitar = 2
                    flash('Vuelos disponibles')
                    return render_template('reservarVuelo.html', form = forms, titulo = 'Reserva', destino = destino1, vuelo = lista, habilitar = habilitar, tipo=tipo)
            elegir = request.form.get('eleccion') 
            if len(elegir) != 0:
                database1 = "SELECT capacidad FROM vuelos WHERE codigo=?"
                lista = listadata(database1, elegir)
                pasaje1= escape(request.form['pasaje'])
                cupo = (lista[0][0]-int(pasaje1))
                if(cupo<0):
                    flash('*Los cupos son insuficientes')
                else:
                    habilitar = 1
                    database2 = "UPDATE vuelos SET capacidad = ? WHERE codigo = ?"
                    validar2 = validardata(database2, (cupo, elegir))
                    origen1 = escape(request.form['origen'])
                    destino1 = escape(request.form['destino'])
                    usuario = session['user']
                    calificacion = 0

                    database3 = "SELECT id from reservas"
                    listaid3 = elegirlist(database3)
                    id = 0
                    if len(listaid3)==0:
                        id = 1
                    else:
                        for i in range(len(listaid3)):
                            id = listaid3[i][0] + 1
                    database = "INSERT INTO RESERVAS(id, codigo, usuario, origen, destino, pasajes, calificacion) VALUEs (?, ?, ?, ?, ?, ?, ?)"
                    validar = validardata(database,(id, elegir, usuario, origen1, destino1, pasaje1, calificacion ))
                    if validar!=0:
                        flash(f'Reserva exitosa {elegir}')
                    else:
                        flash('*La reserva no fue posible')
                return render_template('reservarVuelo.html', form = forms, titulo = 'Reserva', elegir=elegir,habilitar = habilitar, tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/usuarioLcalificar', methods=['POST', 'GET'])
def calificarv():
    try:
        tipo = session['type']
        forms = FormCalificar()
        usuario = session['user']
        database1 = "SELECT id, codigo, origen, destino, pasajes, calificacion FROM reservas WHERE usuario=?"
        reservas = listadata(database1, usuario)
        habilitar = 2
        if request.method =="GET":
            return render_template('calificarVuelo.html', form = forms, titulo = 'Calificar', habilitar = habilitar, vuelo=reservas, tipo=tipo)
        if request.method =="POST":
            elegir = request.form.get('eleccion') 
            if len(elegir) != 0:
                calificacion1 = escape(request.form['calificacion'])
                database2 = "UPDATE reservas SET calificacion = ? WHERE id = ?"
                validar2 = validardata(database2, (calificacion1, elegir))
                if validar2 != 0:
                    flash('Calificación registrada')
                    database4 = "SELECT codigo FROM reservas WHERE id=?"
                    lista4 = listadata(database4, elegir)
                    database3 = "SELECT calificacion FROM reservas WHERE codigo=?"
                    lista3 = listadata(database3, lista4[0][0])
                    j=0
                    total=0
                    for i in range(len(lista3)):
                        if lista3[i][0]!=0:
                            j=j+1
                            total = total + lista3[i][0]
                        else:
                            j=1
                    prom = total/j
                    database4 = "UPDATE vuelos SET calificacion_prom = ? WHERE codigo = ?"
                    validar4 = validardata(database4, (prom, lista4[0][0]))
                else:
                    flash('Intente más tarde')
            return render_template('calificarVuelo.html', form = forms, titulo = 'Calificar', tipo=tipo) 
    except:
        return render_template('error.html')
        

@app.route('/home/admin')
def administrador():
    try:
        tipo = session['type']
        return render_template('administrador.html', titulo = 'Administración', tipo=tipo) 
    except:
        return render_template('error.html')    


@app.route('/home/adminLagregarv', methods=['POST', 'GET'])
def agregarv():
    try:
        e1, e2, e3, e4, e5, e6, e7 = " ", " ", " ", " ", " ", " ", " "
        tipo = session['type']
        forms = FormAgregarV()
        forms.piloto.choices = listapilotos(2)
        if request.method == "GET":
            return render_template('agregarVuelo.html', form = forms, titulo = 'Agregar', tipo=tipo)
        else:
            codigo1 = escape(request.form['codigo'])
            avion1 = escape(request.form['avion'])
            origen1 = escape(request.form['origen'])
            destino1 = escape(request.form['destino'])
            piloto1 = escape(request.form['piloto'])
            cupo1 = escape(request.form['cupo'])
            estado1 = escape(request.form['estado'])

            verror = False

            if codigo1==None or len(codigo1)==0:
                verror = True
                e1 = "- codigo -"
            if avion1==None or len(avion1)==0:
                verror = True
                e2 = "- avion -"
            if origen1==None or len(origen1)==0:
                verror = True
                e3 = "- origen -"
            if destino1==None or len(destino1)==0:
                verror = True
                e4 = "- destino -"
            if piloto1==None or len(piloto1)==0:
                verror = True
                e5 = "- piloto -"
            if cupo1==None or len(cupo1)==0:
                verror = True
                e6 = "- cupo -"
            if estado1==None or estado1=='None':
                verror = True
                e7 = "- estado -"
            if (verror):
                flash('*Validar: {}{}{}{}{}{}{}'.format(e1,e2,e3,e4,e5,e6,e7))

            if not verror:
                database = "INSERT INTO VUELOS(codigo, avion, origen, destino, piloto , capacidad, estado, calificacion_prom) VALUEs (?, ?, ?, ?, ?, ?, ?, ?)"

                validar = validardata(database,(codigo1, avion1, origen1, destino1, piloto1, cupo1, estado1, 0))
                if validar!=0:
                    flash('Vuelo creado con éxito')
                else:
                    flash('*El código de vuelo ya existe, intente con otro')

            return render_template('agregarVuelo.html', form = forms, titulo = 'Agregar', tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/adminLeliminarV', methods=['POST', 'GET'])
def eliminarv():
    try:
        tipo = session['type']
        forms = FormEliminarV()
        habilitar = 0
        if request.method == "GET":
            return render_template('eliminarVuelo.html', form = forms, titulo = 'Eliminar', habilitar=habilitar, tipo=tipo)
        
        else:
            if request.form.get('enviar') == 'Buscar':
                codigo1 = escape(request.form['codigo'])
                database = "SELECT codigo, avion, origen, destino, piloto, capacidad, estado FROM vuelos WHERE codigo=?"
                lista = listadata(database, codigo1)
                
                if len(lista)==0:
                    flash('*El vuelo no está registrado')
                    return render_template('eliminarVuelo.html', form = forms, titulo = 'Eliminar', tipo=tipo)
                elif len(lista)!=0:
                    flash('El vuelo encontrado')
                    habilitar = 1
                    return render_template('eliminarVuelo.html', form = forms, titulo = 'Eliminar', vuelo=lista, habilitar=habilitar, tipo=tipo)
                
            elif request.form.get('eliminar') == 'Eliminar':
                codigo1 = escape(request.form['codigo'])
                database = "DELETE from vuelos where codigo =?"
                eliminar = eliminardata(database, codigo1)
                if eliminar==0:
                    flash('*No fue posible eliminar el vuelo')
                    return render_template('eliminarVuelo.html', form = forms, titulo = 'Eliminar', tipo = tipo)
                elif eliminar!=0:
                    flash('Vuelo eliminado')
                    habilitar = 0
                    return render_template('eliminarVuelo.html', form = forms, titulo = 'Eliminar', habilitar=habilitar, tipo = tipo)
    except:
        return render_template('error.html')

@app.route('/home/adminLeditarv', methods=['POST', 'GET'])
def editarv():
    try:
        e1,e2,e3,e4,e5,e6,e7 = "","","","","","",""
        habilitar = 1
        tipo = session['type']
        forms = FormEditarV()
        forms.piloto.choices = listapilotos(2)
        if request.method == "GET":
            return render_template('editarVuelo.html', form = forms, titulo = 'Editar', habilitar=habilitar, tipo=tipo)
        else:
            if request.form.get('buscar') == 'Buscar':
                codigo1 = escape(request.form['codigo'])
                database = "SELECT codigo, avion, origen, destino, piloto, capacidad, estado FROM vuelos WHERE codigo=?"
                lista = listadata(database, codigo1)
                if len(lista)==0:
                    flash('*El vuelo no está registrado')
                    return render_template('editarVuelo.html', form = forms, titulo = 'Editar', tipo=tipo)
                elif len(lista)!=0:
                    habilitar = 2
                    flash('El vuelo encontrado')
                    forms.avion.data = lista[0][1]
                    forms.origen.data = lista[0][2]
                    forms.destino.data = lista[0][3]
                    forms.piloto.data = lista[0][4]
                    forms.cupo.data = int(lista[0][5])
                    forms.estado.data = lista[0][6]
                    return render_template('editarVuelo.html', form = forms, titulo = 'Editar', habilitar=habilitar, tipo=tipo)
            elif request.form.get('enviar') == 'Editar':
                codigo1 = escape(request.form['codigo'])
                avion1 = escape(request.form['avion'])
                origen1 = escape(request.form['origen'])
                destino1 = escape(request.form['destino'])
                piloto1 = escape(request.form['piloto'])
                cupo1 = escape(request.form['cupo'])
                cupo2 = int(cupo1)
                estado1 = escape(request.form['estado'])

                verror = False

                if codigo1==None or len(codigo1)==0:
                    verror = True
                    e1 = "- codigo -"
                if avion1==None or len(avion1)==0:
                    verror = True
                    e2 = "- avion -"
                if origen1==None or len(origen1)==0:
                    verror = True
                    e3 = "- origen -"
                if destino1==None or len(destino1)==0:
                    verror = True
                    e4 = "- destino -"
                if piloto1==None or len(piloto1)==0:
                    verror = True
                    e5 = "- piloto -"
                if cupo2==None or cupo2<0:
                    verror = True
                    e6 = "- cupo -"
                if estado1==None or estado1=='None':
                    verror = True
                    e7 = "- estado -"
                if (verror):
                    flash('*Validar: {}{}{}{}{}{}{}'.format(e1,e2,e3,e4,e5,e6,e7))

                if not verror:
                    database = "UPDATE vuelos SET (avion, origen, destino, piloto, capacidad, estado) = ( ?,?,?,?,?,? ) WHERE codigo = ?"
                    validar = validardata(database, (avion1,origen1,destino1, piloto1,cupo2,estado1, codigo1))
                    if validar!=0:
                        flash('Vuelo actualizado con éxito')
                        habilitar = 1
                    else:
                        flash('*El vuelo no se pudo actualizar')
                        habilitar = 2
            return render_template('editarVuelo.html', form = forms, titulo = 'Editar', habilitar = habilitar, tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/comentario', methods=['POST', 'GET'])
def comentario():
    try:
        usuario = session['user'] 
        habilitar = 1
        tipo = session['type']
        forms = FormComentar()
        if request.method =="GET":
            return render_template('gestionComent.html', form = forms, titulo = 'Comentario', habilitar=habilitar, tipo=tipo)
        if request.method =="POST":
            if request.form.get('buscar') == 'Buscar':
                codigo1 = escape(request.form['buscarCom'])
                database = "SELECT motivo, comentario FROM comentarios WHERE id=?"
                lista = listadata(database, codigo1)
                if len(lista)==0:
                    habilitar = 1
                    flash('*El comentario no está registrado')
                    return render_template('gestionComent.html', form = forms, titulo = 'Comentario', habilitar=habilitar, tipo=tipo)
                elif len(lista)!=0:
                    habilitar = 2
                    flash('El comentario encontrado')
                    forms.motivo.data = lista[0][0]
                    forms.comentario.data = lista[0][1]
                    return render_template('gestionComent.html', form = forms, titulo = 'Comentario', habilitar=habilitar, tipo=tipo)

            if request.form.get('editar') == 'Editar':
                codigo1 = escape(request.form['buscarCom'])
                motivo1 = escape(request.form['motivo'])
                comentario1 = escape(request.form['comentario'])
                e1, e2 = " ", " "
                verror = False
                if motivo1==None or len(motivo1)==0:
                    verror = True
                    e1 = "- motivo -"
                if comentario1==None or len(comentario1)==0:
                    verror = True
                    e2 = "- comentario -"
                if (verror):
                    flash('*Validar: {}{}'.format(e1,e2))
                if not verror:
                    database = "UPDATE comentarios SET (motivo, comentario, editado) = ( ?,?,? ) WHERE id = ?"
                    validar = validardata(database, (motivo1, comentario1,usuario, codigo1))
                    if validar!=0:
                        habilitar = 1
                        flash('Comentario actualizado con exitó')
                    else:
                        habilitar = 2
                        flash('*El comentario no se pudo actualizar')
                return render_template('gestionComent.html', form = forms, titulo = 'Comentario', habilitar=habilitar, tipo=tipo)

            if request.form.get('eliminar') == 'Eliminar':
                codigo1 = escape(request.form['buscarCom'])
                database = "DELETE from comentarios where id =?"
                eliminar = eliminardata(database, codigo1)
                if eliminar==0:
                    flash('*No fue posible eliminar el comentario')
                    return render_template('gestionComent.html', form = forms, titulo = 'Comentario', tipo=tipo)
                elif eliminar!=0:
                    flash('Comentario eliminado')
                    return render_template('gestionComent.html', form = forms, titulo = 'Comentario', tipo=tipo)

            if request.form.get('enviar') == 'Enviar':
                e1,e2 = "",""
                motivo1 = escape(request.form['motivo'])
                comentario1 = escape(request.form['comentario'])

                verror = False
                if motivo1==None or len(motivo1)==0:
                    verror = True
                    e1 = "- Motivo -"
                if comentario1==None or len(comentario1)==0:
                    verror = True
                    e2 = "- Comentario -"
                if (verror):
                    flash('*Validar: {}{}'.format(e1,e2))

                if not verror:
                    database = "SELECT id from comentarios"
                    listaid = elegirlist(database)
                    id = 0
                    if len(listaid)==0:
                        id = 1
                    else:
                        for i in range(len(listaid)):
                            id = listaid[i][0] + 1
                
                    database1 = "INSERT INTO COMENTARIOS(id, usuario, motivo, comentario, editado) VALUEs (?, ?, ?, ?, ?)"
                    validar = validardata(database1,(id, usuario, motivo1, comentario1, usuario))
                    if validar!=0:
                        flash(f'Mensaje registrado con id = {id}')
                    else:
                        flash('*Intente de nuevo')
                return render_template('gestionComent.html', form = forms, titulo = 'Comentario', tipo=tipo)
    except:
        return render_template('error.html')
        

@app.errorhandler(404)
def error404(error):
    try:
        tipo = session['type']
        return render_template('error.html', tipo=tipo)
    except:
        return render_template('error.html', tipo=tipo)

@app.route('/registroAdmin', methods=['POST', 'GET'])
def registroadmin():
    try:
        tipo = session['type']
        e1, e2, e3, e4, e5, e6, e7 = " ", " ", " ", " ", " ", " ", " "
        forms = FormRegistroAdmin()
        if request.method == "GET":
            return render_template('registroadmin.html', form = forms, titulo = "Registro", tipo = tipo)
        else:
            nombre1 = escape(request.form['nombre'])
            cedula1 = escape(request.form['cedula'])
            correo1 = escape(request.form['correo'])
            telefono1 = escape(request.form['telefono'])
            usuario1 = escape(request.form['usuario'])
            contrasena1 = escape(request.form['contrasena'])
            aceptar1 = escape(request.form.get('aceptar'))
            tipo = escape(request.form['tipo'])
        
            verror = False

            if nombre1==None or len(nombre1)==0:
                verror = True
                e1 = "- nombre -"
            if cedula1==None or len(cedula1)==0:
                verror = True
                e2 = "- cédula -"
            if correo1==None or len(correo1)==0:
                verror = True
                e3 = "- correo -"
            if telefono1==None or len(telefono1)==0:
                verror = True
                e4 = "- teléfono -"
            if usuario1==None or len(usuario1)==0:
                verror = True
                e5 = "- usuario ej:aA123456 -"
            if contrasena1==None or len(contrasena1)==0:
                verror = True
                e6 = "- contraseña ej:aA123456 -"
            if aceptar1==None or aceptar1=='None':
                verror = True
                e7 = "- aceptar condiciones -"
            if (verror):
                flash('*Validar: {}{}{}{}{}{}{}'.format(e1,e2,e3,e4,e5,e6,e7))

            if not verror:
                database = "INSERT INTO USUARIOS(nombre, cedula, correo, telefono, usuario, contraseña, tipo, aceptar) VALUEs (?, ?, ?, ?, ?, ?, ?, ?)"
                password = generate_password_hash(contrasena1)
                validar = validardata(database,(nombre1, cedula1, correo1, telefono1, usuario1, password, tipo, aceptar1))
                if validar!=0:
                    flash('Datos almacenados con exitó')
                else:
                    flash('*El usuario ya existe, intente con otro')
            return render_template('registroadmin.html', form = forms, titulo = "Registro", tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/perfil')
def perfil():
    try:
        nombre = session['name']
        usuario = session['user']
        cedula = session['id']
        correo = session['email']
        telefono = session['phone']
        tipo = session['type']
        lista = (nombre, usuario, cedula, correo, telefono, tipo)
        return render_template('perfil.html', titulo = "Perfil", lista=lista, tipo=tipo)
    except:
        return render_template('error.html')

@app.route('/home/vueloPiloto')
def vuelospiloto():
    try:
        tipo = session['type']
        nombre = session['name']
        database = "SELECT codigo, avion, origen, destino, piloto, capacidad, estado FROM vuelos WHERE piloto=?"
        lista = listadata(database, nombre)
        if len(lista)==0:
            flash('*No tiene vuelos')
            return render_template('vuelosPiloto.html', titulo = 'Pilotos', tipo=tipo)
        elif len(lista)!=0:
            flash('Vuelos asignados')
            print(lista)
            return render_template('vuelosPiloto.html', titulo = 'Pilotos', vuelo = lista, tipo=tipo)
    except:
        return render_template('error.html')