import os
from flask import request 
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from app.models import Post, Follow
from app.cache import cache

# -----------------------------------------------------------

class FeedAPI(Resource): 

    @jwt_required()
    @cache.cached(timeout=300, key_prefix=lambda: f"feed_data_{get_jwt_identity()}")

    def get(self):
        current_user = get_jwt_identity()

        # Get a list of the user's followed users
        followed_users = Follow.query.filter(Follow.follower.has(id=current_user)).all()

        # Get the list of user ids for the user's followed users
        followed_user_ids = [followed_user.followed_id for followed_user in followed_users]

        # Add the current user's id to the list of followed user ids
        followed_user_ids.append(current_user)

        # Get all the posts of the followed users, ordered by timestamp
        posts = Post.query.filter(Post.user_id.in_(followed_user_ids)).order_by(Post.timestamp.desc()).all()

        # Format the posts data into a list of dictionaries
        feedposts_data = []
        
        for post in posts:
            post_data = {}

            if post.image:
                image_dir, image_filename = os.path.split(post.image)

                image_path = os.path.join("static", "posts", image_filename)

                post_data['image'] = image_path

            else:
                post_data['image'] = None

            # ---------

            post_image_url = None
            if post.image:
                post_image_url = f"{request.host_url}{image_path}"

            # ----------

            post_data['id'] = post.id
            post_data['username'] = post.user.username
            post_data['title'] = post.title
            post_data['caption'] = post.caption
            post_data['image'] = post.image
            post_data['post_image_url'] = post_image_url
            post_data['timestamp'] = post.timestamp.isoformat()
            post_data['feed_post_count'] = len(posts),

            post_comments = post.comments.all()
            post_data['comments_count'] = len(post_comments)

            post_data['comments'] = [{
                'username': comment.user.username,
                'content': comment.content,
                'timestamp': comment.timestamp.isoformat()
            } for comment in post_comments]


            # Check if the post has been updated
            if post.timestamp == post.last_updated:
                post_data['last_updated'] = None
            else:
                post_data['last_updated'] = post.last_updated.isoformat()

            feedposts_data.append(post_data)

        # Return the posts data as a JSON response
        return {'status': 'success', 'data': feedposts_data}, 200