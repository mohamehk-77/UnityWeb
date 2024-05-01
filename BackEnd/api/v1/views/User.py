from flask import Blueprint, request, jsonify
from Create import Users
from Create import add_user, edit_user_name, session

User_app_views = Blueprint('User_app_views', __name__)


@User_app_views.route('/users', methods=['POST'])
def CreateUser():
    Data = request.get_json()    
    add_user(Data['FirstName'], Data['LastName'],
             Data['Gender'], Data['ProfileName'],
             Data['Email'], Data['Password'])
    return jsonify({"message": "User Created Successfully"}), 201


@User_app_views.route("/users/<userID>", methods=["PUT"])
def UpdateUserName(userID):
    Data = request.get_json()
    edit_user_name(userID, Data.get('new_first_name'),
                   Data.get('new_last_name'))
    return jsonify({"message": "User Updated Successfully"}), 200


@User_app_views.route("/users/<userID>", methods=["GET"])
def GetUser(userID):
    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        return jsonify({"FirstName": User.FirstName,
                        "LastName": User.LastName,
                        "Gender": User.Gender,
                        "Email": User.Email}), 200
    else:
        return jsonify({"message": "User Not Found"}), 404


@User_app_views.route("/users/<userID>", methods=["DELETE"])
def DeleteUser(userID):
    User = session.query(Users).filter_by(userID=userID).first()
    if User:
        session.delete(User)
        session.commit()
        return jsonify({"message": "User Deleted Successfully!"}), 200
    else:
        return jsonify({"message": "User Not Found!"}), 404
