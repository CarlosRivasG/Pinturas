
import os

from flask import flash
from flask_crud.config.mysqlconnection import connectToMySQL
from flask_crud.models.modelo_base import ModeloBase


from flask_crud.utils.regex import REGEX_CORREO_VALIDO

class Pintura(ModeloBase):

    modelo = 'pinturas'
    campos = ['titulo','descricion','precio','nombre_usuario', 'usuario_creador']

    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.precio = data['precio']
        self.nombre_usuario = data['nombre_usuario']
        self.usuario_creador = data['usuario_creador']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_id_user(cls, id):
        query = f"SELECT * FROM pinturas JOIN usuarios ON usuarios.id = pinturas.usuario_creador WHERE pinturas.id = %(id)s" 
        data = {'id': id,
        }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query,data)
        print("AQUI QUIERO VER -->",results)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data

    @classmethod
    def get_by_id2(cls, id):
        query = f"SELECT pinturas.*, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS nombre_usuario  FROM pinturas JOIN usuarios  on usuarios.id = usuario_creador WHERE usuario_creador = %(id)s"
        data = { 'id' : id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print(results)
        return cls(results[0])
    
    @classmethod
    def get_by_id3(cls, id):
        query = f"SELECT pinturas.* FROM pinturas WHERE pinturas.id = %(id)s"
        data = { 'id' : id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print(results)
        return results

    @classmethod
    def validar_pintura(cls, data):

            is_valid = True

            is_valid = cls.validar_largo(data, 'titulo', 2)
            is_valid = cls.validar_largo(data, 'descripcion', 10)
            is_valid = cls.validar_cantidad(data, 'precio', 0)
            return is_valid

    

    @classmethod
    def get_all_pinturas(cls):
        query = f"SELECT pinturas.*, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS nombre_usuario FROM pinturas JOIN usuarios  ON usuarios.id = usuario_creador"
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data

    @classmethod
    def save_pintura(cls, data):
        query = f"INSERT INTO pinturas (titulo, descripcion,precio, usuario_creador,created_at, updated_at) VALUES( %(titulo)s ,%(descripcion)s,%(precio)s ,%(usuario_creador)s,NOW(),NOW())"

                
        print(query)
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @classmethod
    def update_pintura(cls,data):
        query = """UPDATE pinturas
                        SET titulo= %(titulo)s,
                        descripcion = %(descripcion)s, precio = %(precio)s WHERE id =  %(id)s;"""
        print(query)
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        print("RESULTADO: ", resultado)
        return resultado

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM pinturas WHERE id = %(id)s";
        result = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return cls(result[0])

