from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User, Follow, db

# -----------------------------------------------------------

class FollowAPI(Resource):
    @jwt_required()
    def post(self, username):
        current_user_id = get_jwt_identity()

        if current_user_id is None:
            return {'message': 'Invalid or expired token !!'}, 401

        # get the current user. 
        current_user = User.query.get(current_user_id)

        # get the user to follow.
        user = User.query.filter_by(username=username).first()

        print(current_user)
        print(user)

        # check if this user exists.
        if user is None:
            return {'status': 'fail', 'message': f'User "{username}" not found'}, 404
        
        if user == current_user: 
            return {'status': 'fail', 'message': 'You cannot follow yourself !!'}

        if current_user.is_following(user):
            return {'status': 'fail', 'message': f'You are already following {username}'}, 400
        
        # follow the user.
        current_user.follow(user)
        db.session.flush()

        return {'status': 'success', 'message': f'You are now following {username} !!'}, 201