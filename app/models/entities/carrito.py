from __init__ import dbalchemy as db

class Carrito(db.model):
    id_carrito = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.TIMESTAMP, nullable=False)
