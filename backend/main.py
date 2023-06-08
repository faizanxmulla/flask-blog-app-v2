from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

import app.config as config
from app.cache import cache
from app.security import user_datastore, security
from app.models import db

# CELERY related imports 
from app import workers
from app.tasks import *

from flask_static_digest import FlaskStaticDigest

# importing API's
from api.auth.registerAPI import RegisterAPI
from api.auth.loginAPI import LoginAPI
from api.auth.loginAPI import RefreshTokenAPI

from api.posts.postAPI import PostAPI
from api.posts.feedAPI import FeedAPI

from api.users.userAPI import UserAPI
from api.profile.profileAPI import ProfileAPI

from api.comment.commentAPI import CommentAPI

from api.follow.followAPI import FollowAPI
from api.follow.unfollowAPI import UnfollowAPI
from api.follow.followersAPI import FollowersAPI
from api.follow.followingAPI import FollowingAPI
from api.export.exportAPI import ExportAPI


# -----------------

app = Flask(__name__)
app.config.from_object(config)
app.app_context().push()

# -----------------

# Flask CORS 
CORS(app, supports_credentials=True)

# Add CORS headers to every response
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response

@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response

# ------------------

# database initialization
db.init_app(app)

# API initialization
api = Api(app)
api.init_app(app)

# JWT initialization
JWTManager(app)

# Flask Security
security.init_app(app, user_datastore)

# Flask Caching
cache.init_app(app)


# CELERY -----------

celery = workers.celery

celery.conf.update(
    broker = app.config['CELERY_BROKER_URL'],
    backend = app.config['CELERY_RESULT_BACKEND'],
    timezone = 'Asia/Calcutta',
    enable_utc = False
)

celery.Task = workers.ContextTask
app.app_context().push()


# Serve static assets with an efficient cache policy. (LIGHTHOUSE report)

static_digest = FlaskStaticDigest(app)
# static_url = pass

# API - add resource -----------

api.add_resource(RegisterAPI, '/api/register')
api.add_resource(LoginAPI, '/api/login')
api.add_resource(RefreshTokenAPI, '/api/token/refresh')

api.add_resource(PostAPI, '/api/post','/api/post/<int:post_id>')
api.add_resource(FeedAPI, '/api/feed')

api.add_resource(UserAPI, '/api/user')
api.add_resource(ProfileAPI, '/api/profile/<username>')

api.add_resource(CommentAPI, '/api/post/<int:post_id>/comment', '/api/post/<int:post_id>/comment/<int:comment_id>')

api.add_resource(FollowAPI, '/api/follow/<username>')
api.add_resource(UnfollowAPI, '/api/unfollow/<username>')
api.add_resource(FollowersAPI, '/api/followers/<username>')
api.add_resource(FollowingAPI, '/api/following/<username>')

api.add_resource(ExportAPI, '/api/export-posts-csv')

# --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)


