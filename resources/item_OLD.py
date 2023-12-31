# import uuid
# from flask import request
# from flask.views import MethodView
# from flask_smorest import abort,Blueprint
# from db import items
# from schemas import ItemSchema,ItemUpdateSchema

# blp = Blueprint("Items","item",description="Operations on items")

# @blp.route("/items/<string:item_id>")
# class Store(MethodView):
#     @blp.response(200, ItemSchema)
#     def get(self,item_id):
#         try:
#           return items[item_id]
#         except KeyError as e:
#           abort(404,message="item not found!") 

#     def delete(self,item_id):
#         try:
#           del items[item_id]
#           return {"Message":"Item deleted"}
#         except KeyError:
#            abort(404,message="Item not found!")
    
#     @blp.arguments(ItemUpdateSchema)
#     @blp.response(200, ItemSchema)
#     def put(self,item_data,item_id): #--> Ricordati che,quando usi gli schemas, il parametro extra va PRIMA di tutti gli altri!
#         # item_data=request.get_json()
#         # if "price" not in item_data or "name" not in item_data:
#         #  abort(400,message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
#         try:
#           item=items[item_id]
#           item |= item_data #Inplace operation between objects! update operation between dictionaries!
#           return item
#         except KeyError:
#           abort(404,message="item not found!")
        

# @blp.route("/items")
# class StoreList(MethodView):
#     @blp.response(200, ItemSchema(many=True))
#     def get(self):
#         return items.values()

#     @blp.arguments(ItemSchema)
#     @blp.response(201, ItemSchema)
#     def post(self,item_data):
#     #  item_data = request.get_json() --> Possiamo eliminarlo grazie a ItemSchema!
#     # Here not only we need to validate data exists,
#     # But also what type of data. Price should be a float,
#     # for example.
#      if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#      ):
#         abort(
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#      for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists.")

#      item_id = uuid.uuid4().hex
#      item = {**item_data, "id": item_id}
#      items[item_id] = item

#      return item

    









































