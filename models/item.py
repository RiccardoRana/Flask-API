from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50))
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey("stores.id"),unique=True, nullable=False)
    store = db.relationship("StoreModel",back_populates="items") #Collega al modello dell'item un oggetto de modello dello store, così quando abbiamo l'id come chiave esterna, raggiungiamo anche lo store!
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    

    























