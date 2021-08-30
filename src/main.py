"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/usuario/crear', methods=['POST'])
#Decorador (ruta, metodo)
def crear_usuario():
#    nombre de la funcion
#    solicitud parametro 
    tipo = request.json["tipo"]
    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    sexo = request.json["sexo"]
    correo = request.json["correo"]
    clave = request.json["clave"]
    telefono = request.json["telefono"]
    ciudad = request.json["ciudad"]
    rrss = request.json["rrss"]
    
    nuevo_usuario= Usuario(tipo=tipo, nombre=nombre, apellido=apellido, sexo=sexo, correo=correo, clave=clave, telefono=telefono , ciudad=ciudad, rrss=rrss ) 
    # crear nuevo con el clase Usuario
    db.session.add(nuevo_usuario)
    #agregar a la bd el nuevo usuario
    db.session.commit()
    #guardar en la bd el nuevo usuario
    return jsonify(nuevo_usuario.serialize())
#retorna, jsonify convierte en Json la respuesta y serialize pasa todos los campos del modelo dezglosa.

@app.route('/usuario/<id>', methods=['GET'])
def obtener_usuario(id):
    usuario_obtenido= Usuario.query.get(id) 
    return jsonify(usuario_obtenido.serialize())

@app.route('/usuario/<id>', methods=['PUT'])

def actualizar_usuario(id):
    usuario_obtenido= Usuario.query.get(id)

    usuario_obtenido.tipo = request.json["tipo"]
    usuario_obtenido.nombre = request.json["nombre"]
    usuario_obtenido.apellido = request.json["apellido"]
    usuario_obtenido.sexo = request.json["sexo"]
    usuario_obtenido.correo = request.json["correo"]
    usuario_obtenido.clave = request.json["clave"]
    usuario_obtenido.telefono = request.json["telefono"]
    usuario_obtenido.ciudad = request.json["ciudad"]
    usuario_obtenido.rrss = request.json["rrss"]
    
    db.session.commit()
    return jsonify(usuario_obtenido.serialize())

@app.route('/usuario/<id>', methods=['DELETE'])

def Borrar_usuario(id):
    usuario_obtenido= Usuario.query.get(id)
    
    db.session.delete(usuario_obtenido)
    db.session.commit()
    return jsonify({ "message": 'Usuario eliminado satisfactoriamente'})


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
