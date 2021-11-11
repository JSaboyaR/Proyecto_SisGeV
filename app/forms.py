from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from dataBase import listadata


def listapilotos(tipo) ->list:
    database = "SELECT nombre FROM usuarios WHERE tipo=?"
    lista = listadata(database, tipo)
    pilotos = [("","")]
    if(len(lista)!=0):
        for i in range(len(lista)):
            piloto = (lista[i][0],lista[i][0])
            pilotos.append(piloto)
    else:
        pilotos=[("","")]
    return pilotos


mensaje = "Campo Requerido"
pilotos = listapilotos(2)


class FormLogin(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(mensaje)])
    contrasena = PasswordField('Contraseña', validators=[DataRequired(mensaje)])
    enviar = SubmitField('Ingresar')


class FormRegistro(FlaskForm):
    nombre = StringField('Nombre * ', validators=[DataRequired(mensaje)])
    cedula = StringField('Cedula * ', validators=[DataRequired(mensaje)])
    correo = EmailField('Correo * ', validators=[DataRequired(mensaje)])
    telefono = StringField('Teléfono * ', validators=[DataRequired(mensaje)])
    usuario = StringField('Usuario * ', validators=[DataRequired(mensaje)])
    contrasena = PasswordField('Contraseña * ', validators=[DataRequired(mensaje)])
    aceptar = BooleanField(' Acepta la política de seguridad y tratamiento de los datos personales', validators=[DataRequired(mensaje)])
    enviar = SubmitField('Registrarse')


class FormBuscarV(FlaskForm):
    codigoB = StringField('Código del vuelo * ', validators=[DataRequired(mensaje)])
    enviar = SubmitField('Buscar')


class FormReservar(FlaskForm):
    origen = SelectField(u'Origen * ', choices=[('', ''),('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali'),])
    destino = SelectField(u'Destino * ', choices=[('', ''),('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali'),])
    pasaje = SelectField(u'N° Tickets * ', choices=[(1, 1),(2, 2), (3, 3), (4, 4), (5, 5),])
    buscar = SubmitField('Buscar')
    eleccion = SubmitField('Eleccion')

class FormCalificar(FlaskForm):
    eleccion = SubmitField('Eleccion')
    calificacion = SelectField(u'Calificación asignada al vuelo * ', choices=[(1, '★ 1'),(2, '★ 2'), (3, '★ 3'), (4, '★ 4'), (5, '★ 5'),])

class FormAgregarV(FlaskForm):
    codigo = StringField('Código * ', validators=[DataRequired(mensaje)])
    avion = StringField('Avión * ', validators=[DataRequired(mensaje)])
    origen = SelectField(u'Origen * ', choices=[('', ''),('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali'),])
    destino = SelectField(u'Destino * ', choices=[('', ''),('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali'),])
    piloto = SelectField(u'Piloto * ', choices = pilotos)
    cupo = SelectField(u'Capacidad * ', choices=[(0, 0),(10, 10), (20, 20), (30, 30), (40, 40), (50, 50)])
    estado = SelectField(u'Estados * ', choices=[('', ''),('a tiempo', 'a tiempo'), ('retasado', 'retasado'), ('aterrizado', 'aterrizado'), ('despegado', 'despegado'),])
    enviar = SubmitField('Crear Vuelo')


class FormEliminarV(FlaskForm):
    codigo = StringField('Código del vuelo * ', validators=[DataRequired(mensaje)])
    enviar = SubmitField('Buscar')
    eliminar = SubmitField('Eliminar')

class FormEditarV(FlaskForm):
    codigo = StringField('Código de vuelo a editar * ', validators=[DataRequired(mensaje)])
    avion = StringField('Avión *', validators=[DataRequired(mensaje)])
    origen = SelectField('Origen *', choices=[('', ''), ('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali')])
    destino = SelectField('Destino *', choices=[('', ''), ('Pasto', 'Pasto'), ('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cali', 'Cali')])
    piloto = SelectField('Piloto *', choices=pilotos)
    cupo = StringField('Capacidad *', validators=[DataRequired(mensaje)])
    estado = SelectField('Estados *', choices=[('', ''),('a tiempo', 'a tiempo'), ('retasado', 'retasado'), ('aterrizado', 'aterrizado'), ('despegado', 'despegado')])
    buscar = SubmitField('Buscar')
    enviar = SubmitField('Editar')

class FormComentar(FlaskForm):
    buscarCom = StringField('Comentario a buscar ', validators=[DataRequired(mensaje)])
    motivo = SelectField(u'Motivo del comentario ', choices=[('petición', 'petición'), ('queja', 'queja'), ('reclamos', 'reclamos'), ('sugerencia', 'sugerencia')])  
    comentario = TextAreaField('Ingresa aquí tu comentario ', validators=[DataRequired(mensaje)])
    editar = SubmitField('Editar')
    buscar = SubmitField('Buscar')
    enviar = SubmitField('Enviar')
    eliminar = SubmitField('Eliminar')

class FormRegistroAdmin(FlaskForm):
    nombre = StringField('Nombre * ', validators=[DataRequired(mensaje)])
    cedula = StringField('Cedula * ', validators=[DataRequired(mensaje)])
    correo = EmailField('Correo * ', validators=[DataRequired(mensaje)])
    telefono = StringField('Telefono * ', validators=[DataRequired(mensaje)])
    usuario = StringField('Usuario * ', validators=[DataRequired(mensaje)])
    contrasena = PasswordField('Contraseña * ', validators=[DataRequired(mensaje)])
    tipo = SelectField(u'Tipo * ', choices=[(1, 'Administrativo'), (2, 'Piloto'), (3, 'Usuario')])
    aceptar = BooleanField(' Acepta la política de seguridad y tratamiento de los datos personales', validators=[DataRequired(mensaje)])
    enviar = SubmitField('Registrarse')