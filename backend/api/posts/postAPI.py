import json
import os

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended.utils import create_access_token

from app.models import db, Post, Comment, Follow
from app.utils.save_post import save_post
from app.config import ALLOWED_IMAGE_EXTENSIONS
from app.cache import cache

# ---------------------------------------------------------------

class PostAPI(Resource):

    @jwt_required()
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        
        if post:
            post_data = {}
            post_data['username'] = post.user.username
            post_data['image'] = post.image
            post_data['title'] = post.title
            post_data['caption'] = post.caption
            post_data['timestamp'] = post.timestamp.isoformat()

            post_data['comments'] = [{
                'username': comment.user.username,
                'content': comment.content,
                'timestamp': comment.timestamp.isoformat()
            } for comment in post.comments.all()]

            # Check if the post has been updated
            if post.timestamp == post.last_updated:
                post_data['last_updated'] = None
            else:
                post_data['last_updated'] = post.last_updated.isoformat()

            return {'status': 'success', 'data': post_data}, 200
        else:
            return {'status': 'fail', 'message': 'Post not found'}, 404



    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        # Parse the JSON data from the request
        data = json.loads(request.form['data'])
        
        # Extract the data from the JSON object
        title = data.get('title', '').strip()
        caption = data.get('caption', '').strip()

        # Get the image file from the request
        image = request.files.get('image', None)

        # Validate the request data
        if not title:
            return jsonify({'status': 'fail', 'message': 'Title cannot be blank !!'}), 400
        
        if image and not allowed_file(image.filename):
            return jsonify({'status': 'fail', 'message': 'Invalid image file type !!'}), 422

        # Save the image file (if provided)
        image_path = None
        if image:
            image_path = save_post(image)

        # Create a new post
        post = Post(title=title, caption=caption, image=image_path, user_id=current_user)

        # Save the post to the database
        db.session.add(post)
        db.session.commit()

        # Invalidate the cache.
        cache.delete(f"profile_data_{current_user}")
        cache.delete(f"feed_data_{current_user}")

        # Return a success response
        return {'status': 'success', 'message': 'Post created !!'}, 201


    @jwt_required()
    def put(self, post_id):
        current_user = get_jwt_identity()

        # Parse the JSON data from the request
        data = json.loads(request.form['data'])
        
        # Extract the data from the JSON object
        title = data.get('title', '').strip()
        caption = data.get('caption', '').strip()

        # Get the image file from the request
        image = request.files.get('image', None)

        # Validate the request data
        if not title:
            return {'status': 'fail', 'message': 'Title cannot be blank !!'}, 400
        
        if image and not allowed_file(image.filename):
            return {'status': 'fail', 'message': 'Invalid image file type !!'}, 422

        # Get the post to be updated
        post = Post.query.filter_by(id=post_id, user_id=current_user).first()

        if not post:
            return {'status': 'fail', 'message': 'Post not found !!'}, 404
        
        if post.user_id != current_user:
            return {'status': 'fail', 'message': 'You are not authorized to update this post !!'}, 403

        # Update the post
        post.title = title if title else post.title
        post.caption = caption if caption else post.caption

        if image:
            # Save the new image file
            updated_image_path = save_post(image)
            post.image = updated_image_path

        # Save the updated post to the database
        db.session.commit()

        # Invalidate the cache.
        cache.delete(f"profile_data_{current_user}")
        cache.delete(f"feed_data_{current_user}")

        # Return a success response
        return {'status': 'success', 'message': 'Post updated !!'}, 200
    
    

    @jwt_required()
    def delete(self, post_id):
        current_user = get_jwt_identity()

        # Get the post to be deleted
        post = Post.query.filter_by(id=post_id, user_id=current_user).first()

        if not post:
            return {'status': 'fail', 'message': 'Post not found !!'}, 404
        
        if post.user_id != current_user:
            return {'status': 'fail', 'message': 'You are not authorized to update this post !!'}, 403

        # delete the comment associated with the post
        db.session.query(Comment).filter_by(post_id=post_id).delete()

        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()

        # Invalidate the cache.
        cache.delete(f"profile_data_{current_user}")
        cache.delete(f"feed_data_{current_user}")

        # Return a success response
        return {'status': 'success', 'message': 'Post deleted !!'}


# -------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def remove_post(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
