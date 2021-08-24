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