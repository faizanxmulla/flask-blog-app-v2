import json
from sqlalchemy import case
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import db, User
from app.utils.save_profile_pic import save_profile
from app.config import ALLOWED_IMAGE_EXTENSIONS
from app.cache import cache

# ----------------------------------------------------------------

# get --> SEARCH functionality

class UserAPI(Resource):
    # @cache.cached(timeout=300)
    @jwt_required()
    def get(self):
        # Parse the query parameter from the request
        query = request.args.get('query')

        if not query:
            return {'status': 'fail', 'message': 'Query parameter missing !!'}, 400

        # Get the list of usernames that match the query
        users = User.query.filter(User.username.ilike(f'%{query}%')).order_by(case([(User.username.ilike('a%'), 0)], else_=1), User.username).all()

        # Map the user objects to a list of dictionaries
        result = [{'id': user.id, 'username': user.username} for user in users]

        return {'status': 'success', 'data': result}, 200


    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()

        # Parse the JSON data from the request  
        data = json.loads(request.form['data'])

        # Extract the data from the JSON object
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()

        # get the image file from the request 
        profile_image = request.files.get('profile_image', None)

        if not username:
            return {'status': 'fail', 'message': 'Username cannot be blank !!'}, 400
        
        if profile_image and not allowed_file(profile_image.filename):
            return {'status': 'fail', 'message': 'Invalid image file type !!'}, 422

        # get the account to be updated 
        user = User.query.filter_by(id=current_user).first()

        if not user:
            return {'status':'fail', 'message': 'User not found !!'}, 404
        
        if user.id != current_user:
            return {'status': 'fail', 'message': 'You are not authorized to update this account !!'}, 403
        
        # update username and email address
        user.username = username if username else user.username
        user.email = email if email else user.email
        
        if profile_image:
            updated_profile_path = save_profile(profile_image)
            user.profile_image = updated_profile_path

        # Save the updated profile image to the database
        db.session.commit()

        # Invalidate the cache for the 'profile_data' key
        cache.delete('profile_data')

        return {'status': 'success', 'message': 'Account updated successfully !!'}, 200
    

    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()

        # get the account to be deleted 
        user = User.query.filter_by(id=current_user).first()

        if not user:
            return {'status': 'fail', 'message': 'User not found !!'}, 404
        
        if user.id != current_user:
            return {'status': 'fail', 'message': 'You are not authorized to delete this account !!'}, 403
        
        # delete the account from the database 
        db.session.delete(user)
        db.session.commit()

        # Invalidate the cache for the 'profile_data' key
        cache.delete('profile_data')

        # Return a success response
        return {'status': 'success', 'message': 'User deleted !!'}


# -------------------------------------


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
