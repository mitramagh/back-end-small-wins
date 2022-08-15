import uuid
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort
from datetime import datetime
import app
import jwt

from app.models.user import User
# from app.models.user import initialize_db



user_bp = Blueprint("user_bp", __name__)
# with app.app_context():
#     db.create_all()
# initialize_db(app)



@user_bp.route('/register', methods=['POST'])
def signup_user(): 
    data = request.get_json() 
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    db.session.add(new_user) 
    db.session.commit()   
    return jsonify({'message': 'registered successfully'})



@user_bp.route('/login', methods=['POST']) 
def login_user():
    auth = request.authorization  
    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify', 401, {'Authentication': 'login required"'})   

    user = User.query.filter_by(username=auth.username).first()  
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")

        return jsonify({'token' : token})

    return make_response('could not verify',  401, {'Authentication': '"login required"'})


@user_bp.route('/users', methods=['GET'])
def get_all_users(): 

    users = User.query.all()
    result = []  
    for user in users:  
        user_data = {}  
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['public_id'] = user.public_id 
        
        result.append(user_data)  
    return jsonify({'users': result})