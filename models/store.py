from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store",lazy="dynamic") #lazy is for making the model and the relationships less heavy to process! the data model is more efficient! 
                                                                              #very useful when you have more than one relationship!
    
    
    
    
    
    
    
    
    
    