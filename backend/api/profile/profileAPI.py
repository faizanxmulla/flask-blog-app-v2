import os
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User, Post
from app.cache import cache

# -------------------------------------------------------------

class ProfileAPI(Resource):

    @jwt_required()
    # @cache.cached(timeout=300, key_prefix=lambda: f"profile_data_{get_jwt_identity()}")
    
    def get(self, username):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        profile_username = request.view_args['username']
        user = User.query.filter_by(username=profile_username).first()

        if not user:
            return {'status': 'error', 'message': 'User not found'}, 404

        is_following = current_user.is_following(user) if current_user_id else False

        # --------

        # HANDLING profile images. 
        if user.profile_image:
            image_dir, image_filename = os.path.split(user.profile_image)
            image_path = os.path.join("static", "profile", image_filename)

            profile_image = image_path

        # ---------

        profile_image_url = None
        if user.profile_image:
            profile_image_url = f"{request.host_url}{image_path}"

        # ---------

        # Get the user's posts
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()

        # Format the posts data into a list of dictionaries.
        posts_data = []
        comments_count = 0

        for post in posts:
            post_data = {}

            # ---------

            # HANDLING post images.
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
            post_data['title'] = post.title
            post_data['caption'] = post.caption
            post_data['image'] = post.image
            post_data['post_image_url'] = post_image_url
            post_data['timestamp'] = post.timestamp.isoformat()

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

            posts_data.append(post_data)

        # -----------------------------------------

        # Create a dictionary containing the user's data
        profile_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'profile_image': profile_image,
            'profile_image_url': profile_image_url,
            'posts': posts_data,
            'total_posts': len(posts),
            'followers_count': user.followers.count(),
            'following_count': user.following.count(),
            'comments_count': comments_count,
            'is_following': is_following,
            'is_current_user': user.id == current_user_id,
        }

        # Return the user data as a JSON response
        return {'status': 'success', 'data': profile_data}, 200

