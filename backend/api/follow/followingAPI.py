from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User, Follow

# --------------------------------------------------------------

class FollowingAPI(Resource):
    @jwt_required()
    def get(self, username):
        current_user = get_jwt_identity()

        following = User.query.join(Follow, User.id == Follow.followed_id).filter(Follow.follower_id == current_user).order_by(Follow.timestamp.desc()).all()

        following = [{'id': followed.id, 'username': followed.username} for followed in following if followed != current_user]

        return {'status': 'success', 'following': following}, 200
