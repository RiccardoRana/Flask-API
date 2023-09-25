# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import abort,Blueprint
# from db import stores
# from schemas import StoreSchema

# blp = Blueprint("Stores","store",description="Operations on stores")

# @blp.route("/stores/<string:store_id>")
# class Store(MethodView):
#     @blp.response(200, StoreSchema)
#     def get(self,store_id):
#         try:
#           return stores[store_id]
#         except KeyError as e:
#           abort(404,message="Store not found!") 

#     def delete(self,store_id):
#         try:
#           del stores[store_id]
#           return {"Message":"Store deleted"}
#         except KeyError:
#            abort(404,message="Store not found!")


# @blp.route("/stores")
# class StoreList(MethodView):
#     @blp.response(200, StoreSchema(many=True))
#     def get(self):
#         return stores.values()
    
#     @blp.arguments(StoreSchema)
#     @blp.response(201, StoreSchema)
#     def post(self,store_data):
#       # store_data=request.get_json()
#       # if "name" not in store_data:
#       #    return abort(400,message="Ensure 'name' is included in the JSON payload.")
#       for store in stores.values():
#           if store["name"] == store_data["name"]:
#               abort(400,message="Store already exists!")
#       store_id= uuid.uuid4().hex
#       new_store= {**store_data, "id":store_id} #This will destricture the values inside the dictionary store_data and will put them in new_store
#       stores[store_id]=new_store
#       return new_store,201

    












































