from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from app.models import db, User, Follow

# ---------------------------------------------------------

class UnfollowAPI(Resource):
    @jwt_required()
    def post(self, username):
        current_user_id = get_jwt_identity()

        if current_user_id is None:
            return {'message': 'Invalid or expired token !!'}, 401

        # get the current user. 
        current_user = User.query.get(current_user_id)

        # get the user to unfollow.
        user = User.query.filter_by(username=username).first()

        print(current_user)
        print(user)

        if user is None:
            return {'status': 'fail', 'message': f'User {username} not found !!'}, 404

        if user == current_user:
            return {'status': 'fail', 'message': 'You cannot unfollow yourself !!'}, 400

        if not current_user.is_following(user):
            return {'status': 'fail', 'message': f'You are not following {username} !!'}, 400

        # unfollow the user 
        current_user.unfollow(user)
        db.session.flush()

        return {'status': 'success', 'message': f'You are no longer following {username} !!'}, 201
