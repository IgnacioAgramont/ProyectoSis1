from __init__ import dbalchemy as db

class Catalogo(db.model):
    id_catalogo = db.Column(db.Integer, primary_key=True)
    detalle = db.Column(db.String(500), nullable=False)
    