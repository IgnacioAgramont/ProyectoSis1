from __init__ import dbalchemy as db

class Detalle_Pedido(db.Model):
    id_detalle_pedido = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Decimal(7,2), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    id_producto = db.Column(db.Integer, nullable=False)
    id_pedido = db.Column(db.Integer, nullable=False)
    # ForeignKeyConstraints(['id_pedido'], ['pedido.id_pedido'])