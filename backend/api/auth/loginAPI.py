from flask import jsonify
from flask_restful import Resource, reqparse
from flask_security import login_user
from flask_security.utils import verify_password, hash_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity 

from app.models import User
from app.security import user_datastore
from app.cache import cache

# -------------------------------

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username is required !!')
parser.add_argument('password', type=str, required=True, help='Password is required !!')


class LoginAPI(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        password_hash = args.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user is None:
            return {'message': 'User doesn\'t exist !!'}

        if not verify_password(password_hash, user.password_hash):
            return {'message': 'Incorrect password !!'}

        refresh_token = create_refresh_token(identity=user.id)
        access_token = create_access_token(identity=user.id)
        
        login_user(user)

        # delete the cached profile data for the user
        cache.delete(f"profile_data_{user.id}")
        cache.delete(f"feed_data_{user.id}")
        cache.delete(f"comment_data_{user.id}")
        
        return jsonify({'status': 'success','message': 'Successfully logged in !!', 'access_token': access_token, 'refresh_token': refresh_token , "username": username})



class RefreshTokenAPI(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {'access_token': access_token}, 200
