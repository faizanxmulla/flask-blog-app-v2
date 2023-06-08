from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User, Follow

# ------------------------------------------------------------

class FollowersAPI(Resource):
    @jwt_required()
    def get(self, username):
        current_user = get_jwt_identity()

        followers = User.query.join(Follow, User.id == Follow.follower_id).filter(Follow.followed_id == current_user).order_by(Follow.timestamp.desc()).all()

        followers = [{'id': follower.id, 'username': follower.username} for follower in followers if follower != current_user]

        return {'status': 'success','followers': followers}, 200
