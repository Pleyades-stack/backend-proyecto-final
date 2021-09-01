"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Perro, Imagen
from functools import wraps
import jwt, datetime, time
import cloudinary.uploader as uploader

#from models import Person

secret = 'jwt_secret_key'

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = secret
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL')
)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


def autenticacion(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        token = None

        if 'token-acceso' in request.headers:
            token = request.headers['token-acceso']
        if not token:
            return jsonify({'mensaje': 'Se necesita un token de acceso valido'})
        try:  
            data = jwt.decode(token, options={"verify_signature": False})
            autentificacionUsuario = Usuario.query.filter_by(id=data['id']).first()  
        except:  
            return jsonify({'mensaje': 'Token invalido'})  
        return func(autentificacionUsuario, *args,  **kwargs)  
    return decorador 
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
    #Se encripta la contraseña
    claveEncriptada = generate_password_hash(clave, method='sha256')
    telefono = request.json["telefono"]
    ciudad = request.json["ciudad"]
    rrss = request.json["rrss"]
    nuevo_usuario= Usuario(tipo=tipo, nombre=nombre, apellido=apellido, sexo=sexo, correo=correo, clave=claveEncriptada, telefono=telefono , ciudad=ciudad, rrss=rrss ) 
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


@app.route('/usuario/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data['correo'] or not data['clave']:
        return make_response({'Se necesita nombre y clave', 401})
    usuario = Usuario.query.filter_by(correo=data['correo']).first()
    if check_password_hash(usuario.clave, data["clave"]):
        token = jwt.encode({'id': usuario.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return make_response('Verifique sus datos', 401)

@app.route('/perro/crear/', methods=['POST'])
@autenticacion
def crearPerro(user_auth):
    ubicacion=request.json["ubicacion"]
    nombre=request.json["nombre"]
    sexo=request.json["sexo"]
    edad=request.json["edad"]
    peso=request.json["peso"]
    tamaño=request.json["tamaño"]
    raza=request.json["raza"]
    caracter=request.json["caracter"]
    caracteristicas=request.json["caracteristicas"]
    patologias=request.json["patologias"]
    nuevoPerro = Perro(
        usuario_id=user_auth.id, 
        ubicacion=ubicacion,
        nombre=nombre,
        sexo=sexo,
        edad=edad,
        peso=peso,
        tamaño=tamaño,
        raza=raza,
        caracter=caracter,
        caracteristicas=caracteristicas,
        patologias=patologias,
        adoptado=False)
    db.session.add(nuevoPerro)
    db.session.commit()
    return jsonify({'mensaje': 'perro creado con exito'})

@app.route('/perro/editar/<id>', methods=['PUT'])
@autenticacion
def editarPerro(user_auth, id):
    perroActual = Perro.query.get(id)
    if perroActual.usuario_id != user_auth.id:
        return jsonify({'message': 'No es el cuidador de este perro'})
    perroActual.ubicacion = request.json["ubicacion"]
    perroActual.nombre = request.json["nombre"]
    perroActual.sexo = request.json["sexo"]
    perroActual.edad = request.json["edad"]
    perroActual.peso = request.json["peso"]
    perroActual.tamaño = request.json["tamaño"]
    perroActual.raza = request.json["raza"]
    perroActual.caracter = request.json["caracter"]
    perroActual.caracteristicas = request.json["caracteristicas"]
    perroActual.patologias = request.json["patologias"]
    db.session.commit()
    return jsonify(perroActual.serialize())

@app.route('/perro/<id>', methods=['GET'])
def perro(id):
    perroActual = Perro.query.get(id)
    return jsonify(perroActual.serialize())

@app.route('/perros', methods=['GET'])
def perros():
    perros = [perro.serialize() for perro in Perro.query.all()]
    return jsonify({'perros': perros})

@app.route('/perro/adoptado/<id>', methods=['PUT'])
@autenticacion
def perroAdoptado(user_auth, id):
    perroActual = Perro.query.get(id)
    if perroActual.usuario_id != user_auth.id:
        return jsonify({'message': 'No es el cuidador de este perro'})
    perroActual.adoptado = True
    db.session.commit()
    return jsonify(perroActual.serialize())

@app.route('/usuario/perros', methods=['GET'])
@autenticacion
def perrosUsuario(user_auth):
    perrosDeUsuario = [perro.serialize() for perro in Perro.query.filter_by(usuario_id=user_auth.id).all()]
    return jsonify({'perrosUsuario': perrosDeUsuario})

@app.route('/perro/imagen/<id>', methods=['POST'])
@autenticacion
def imagenNueva(user_auth, id):
    image_file = request.files['file']
    #try:
    response = uploader.upload(image_file)
    nuevaImagen = Imagen(url_imagen=response["secure_url"], perro_id=id, public_id=response["public_id"])
    db.session.add(nuevaImagen)
    db.session.commit()
    return jsonify({'message': 'Imagen guardada con exito', 'response': response , "status": 200})
    #except:
     #   return jsonify({'message': 'Ha ocurrido un error'}, 400)

@app.route('/perro/imagen/<id>', methods=['GET'])
def getImagen(id):
    imagenesPerro = [imagen.serialize() for imagen in Imagen.query.filter_by(perro_id=id).all()]
    return jsonify({'imagenes': imagenesPerro})

@app.route('/perro/imagen/<id>', methods=['delete'])
@autenticacion
def borrarImagen(user_auth, id):
    imagenPerro = Imagen.query.get(id)
    response = uploader.destroy(imagenPerro.public_id)
    db.session.delete(imagenPerro)
    db.session.commit()
    return jsonify({"response": response})

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
