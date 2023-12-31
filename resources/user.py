import requests
import os
from flask import current_app
from sqlalchemy import or_
from dotenv import load_dotenv
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt,get_jwt_identity
from blocklist import BLOCKLIST
from db import db
from models.tag import TagModel
from models.store import StoreModel
from models.items_tags import ItemTagModel
from models.item import ItemModel
from models.user import UserModel
from models import UserModel
from schemas import StoreSchema,TagSchema,TagAndItemSchema, UserSchema, UserRegisterSchema
from tasks import send_user_registration_email

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/users/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id): 
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Store deleted"}
    
@blp.route("/register")
class RegisterUser(MethodView):
     @blp.arguments(UserRegisterSchema)
     def post(self,user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        current_app.queue.enqueue(send_user_registration_email,user.email,user.username)

        # queue.enqueue(send_user_registration_email, user.email, user.username)

        return {"message": "User created successfully."}, 201
        # if UserModel.query.filter(
        #     or_(UserModel.username == user_data["username"], UserModel.email == user_data["email"])).first():
        #     abort(409, message="A user with that name already exists.")
        
        # user = UserModel(
        #     username = user_data["username"],
        #     email = user_data["email"],
        #     password = pbkdf2_sha256.hash(user_data["password"])
            
        # )
        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     send_simple_message(to=user.mail, subject="Successfully signed up!", body="Hi {}! You have successfully signed up the flask-api-python!".format(user.username))
        # except IntegrityError:
        #     abort(
        #         400,
        #         message="A user with that name already exists.",
        #     )
        # except SQLAlchemyError:
        #     abort(500, message="An error occurred creating the user.")

        # return user
     

@blp.route("/login")   
class LoginUser(MethodView):
    @blp.arguments(UserSchema)
    # @blp.response(200, UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(404, message="Invalid credentials.")


@blp.route("/logout")
class LogOutUser(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"successfully logged out."}


@blp.route("/refresh")
class UserRefreshToken(MethodView):
    @jwt_required(refresh=True) #Il metodo richiede un refresh token NON un access token!
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token":new_token}






























