from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    tipo= db.Column(db.String(10), unique=False, nullable=False)
    nombre= db.Column(db.String(15), unique=False, nullable=False)
    apellido= db.Column(db.String(15), unique=False, nullable=False)
    sexo= db.Column(db.String(10), unique=False, nullable=False)
    correo= db.Column(db.String(50), unique=True, nullable=False)
    clave= db.Column(db.String(8), unique=False, nullable=False)
    telefono= db.Column(db.String(11), unique=False, nullable=False)
    ciudad= db.Column(db.String(20), unique=False, nullable=False)
    rrss= db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<usuario %r>' % self.nombreusuario

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "sexo": self.sexo,
            "correo": self.correo,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "rrss": self.rrss,
            # do not serialize the password, its a security breach
        }
    

class Perro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, foreign_key=True)
    imagen = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(120), nullable=False)
    nombre = db.Column(db.String(120), nullable=True)
    sexo = db.Column(db.String(60), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    peso = db.Column(db.Integer, nullable=True)
    tamaño = db.Column(db.Integer, nullable=True)
    raza = db.Column(db.String(60), nullable=True)
    caracter = db.Column(db.String(60), nullable=True)
    caracteristicas = db.Column(db.String(180), nullable=True)
    patologias= db.Column(db.String(180), nullable=True)
    adoptado = db.Column(db.Boolean(), nullable=False)
    def __repr__(self):
        return '<Perro %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.usuario_id,
            "imagen": self.imagen,
            "ubicacion": self.ubicacion,
            "nombre": self.nombre,
            "sexo": self.sexo,
            "edad": self.edad,
            "peso": self.peso,
            "tamaño": self.tamaño,
            "raza": self.raza,
            "caracter": self.caracter,
            "caracteristicas": self.caracteristicas,
            "patologias": self.patologias,
            "adoptado": self.adoptado,
        }