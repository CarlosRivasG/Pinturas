import os

from flask import flash
from flask_crud.config.mysqlconnection import connectToMySQL
from flask_crud.models.modelo_base import ModeloBase
from flask_crud.models.pintura import Pintura
from flask_crud.utils.regex import REGEX_CORREO_VALIDO

class Usuario(ModeloBase):

    modelo = 'usuarios'
    campos = ['nombre','apellido','email','password']

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pinturas= []


    @classmethod
    def get_usuario_pintura(cls, data):
        query = "SELECT * FROM usuarios JOIN pinturas ON pinturas.usuario_creador = usuarios.id WHERE usuarios.id = %(usuario_creador)s"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
    
        if len(results) == 0:
            print(results)
            return None 
        usuario_data= {
            'id': results[0]['id'],
            'nombre': results[0]['nombre'],
            'apellido':results[0]['apellido'] , 
            'email':results[0]['email'] ,
            'password':results[0]['password'] ,
            'created_at': results[0]['created_at'],
            'updated_at':results[0]['updated_at']
        }   
        usuario= Usuario(usuario_data)
        all_pinturas =[]


        for data in results:
            print('*'*20)
            print(data)
            pintura_data={
                'id': data['pinturas.id'],
                'titulo': data['titulo'],
                'descripcion': data['descripcion'],
                'precio': data['precio'],
                'nombre_usuario': data['nombre_usuario'],
                'usuario_creador': data['usuario_creador'],
                'created_at': data['pinturas.created_at'],
                'updated_at': data['pinturas.updated_at']
            }
            new_pintura=Pintura(pintura_data)
            all_pinturas.append(new_pintura)
        usuario.pinturas = all_pinturas
        return usuario

    @classmethod
    def buscar(cls, dato):
        query = "select * from usuarios where email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = f" UPDATE `usuarios` SET `nombre` =  %(nombre)s, `apellido` = %(apellido)s, `email` = %(email)s, `password` = %(password)s WHERE `id` =  %(id)s;"
        
    

        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @classmethod
    def validar(cls, data):

        is_valid = True

        is_valid = cls.validar_largo(data, 'nombre', 2)
        is_valid = cls.validar_largo(data, 'apellido', 2)
        is_valid = cls.validar_largo(data, 'password', 8)

        if not REGEX_CORREO_VALIDO.match(data['email']):
            flash('El correo no es válido', 'error')
            is_valid = False

        if data['password'] != data['cpassword']:
            flash('las contraseñas no son iguales', 'error')
            is_valid = False

        if cls.validar_existe('email', data['email']):
            flash('el correo ya fue ingresado', 'error')
            is_valid = False

        return is_valid