import os
import secrets
from db import db
from flask import Flask,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from flask_migrate import Migrate

def create_app(db_url=None):
 
 app = Flask(__name__)
 #LOLOLOLOLOLOL
 app.config["PROPAGATE_EXCEPTIONS"] = True
 app.config["API_TITLE"] = "Stores REST API"
 app.config["API_VERSION"] = "v1"
 app.config["OPENAPI_VERSION"] = "3.0.3"
 app.config["OPENAPI_URL_PREFIX"] = "/"
 app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
 app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
 app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
 app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 db.init_app(app)
 migrate = Migrate(app, db)
 api = Api(app)
 
 app.config["JWT_SECRET_KEY"] = "102998944772438468138208696091431472216"
 jwt = JWTManager(app)
 
 @jwt.token_in_blocklist_loader
 def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

 
 @jwt.additional_claims_loader
 def add_claim_to_jwt(identity):
     if identity == 1:
         return {"is_admin":True}
     return {"is_admin": False}
 
 
 
 @jwt.expired_token_loader
 def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

 @jwt.invalid_token_loader
 def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

 @jwt.unauthorized_loader
 def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

 @jwt.needs_fresh_token_loader
 def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

 @jwt.revoked_token_loader
 def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

 
#  with app.app_context():
#      db.create_all()
 
 

 api.register_blueprint(ItemBlueprint)
 api.register_blueprint(StoreBlueprint)
 app.register_blueprint(TagBlueprint)
 app.register_blueprint(UserBlueprint)
 
 return app
# @app.get("/stores")
# def get_stores():
#     return {"stores":list(stores.values())}
 
# @app.get("/items")
# def get_all_items():
#     return {"items": list(items.values())} 

# @app.get("/stores/<string:store_id>")
# def get_single_store(store_id):
#  try:
#     return stores[store_id]
#  except KeyError as e:
#     return abort(404,message="Store not found!")    

# @app.get("/items/<string:item_id>")
# def get_single_item(item_id):
#  try:
#     return items[item_id]
#  except KeyError as e:
#     return abort(404,message="item not found!")        


# @app.post("/stores")
# def create_store():
#       store_data=request.get_json()
#       if "name" not in store_data:
#          return abort(400,message="Ensure 'name' is included in the JSON payload.")
#       store_id= uuid.uuid4().hex
#       new_store= {**store_data, "id":store_id} #This will destricture the values inside the dictionary store_data and will put them in new_store
#       stores[store_id]=new_store
#       return new_store,201

# @app.post("/items")
# def create_item():
#     item_data = request.get_json()
#     # Here not only we need to validate data exists,
#     # But also what type of data. Price should be a float,
#     # for example.
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists.")

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item

#     return item
  
# @app.delete("/stores/<string:store_id>")
# def delete_store(store_id):
#    try:
#       del stores[store_id]
#       return {"Message":"Store deleted"}
#    except KeyError:
#       abort(404,message="Store not found!")
  
# @app.delete("/items/<string:item_id>")
# def delete_item(item_id):
#    try:
#       del items[item_id]
#       return {"Message":"Item deleted"}
#    except KeyError:
#       abort(404,message="Operation not possible!")
      

# @app.put("/items/<string:item_id>")      
# def update_item(item_id):
#    item_data=request.get_json()
#    if "price" not in item_data or "name" not in item_data:
#       abort(400,message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
#    try:
#       item=items[item_id]
#       item |= item_data #Inplace operation between objects! update operation between dictionaries!
#       return item
#    except KeyError:
#       abort(404,message="item not found!")
   
   
      
# if __name__=="__main__":
#     app.run(debug=True)








































































