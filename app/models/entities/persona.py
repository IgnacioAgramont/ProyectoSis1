from __init__ import dbalchemy as db
class Persona(db.model):
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), primary_key=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    ci = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        return f'<Persona> {self.nombre}'