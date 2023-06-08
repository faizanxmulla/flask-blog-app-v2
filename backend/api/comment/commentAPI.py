import json

from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from app.models import db, Post, Comment
from app.cache import cache

# ---------------------------------------------------------------

class CommentAPI(Resource):

    @jwt_required()
    @cache.cached(timeout=300, key_prefix=lambda: f"comment_data_{get_jwt_identity()}")

    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()

        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()

        comments_data = []

        for comment in comments:
            comment_data = {
                'user_id': comment.user_id,
                'username': comment.user.username,
                'is_current_user': comment.user_id == get_jwt_identity(),
                'post_id': post.id,
                'count' : len(comments),
                'id': comment.id,
                'content': comment.content,
                'timestamp': comment.timestamp.isoformat(),
            }

            # Check if the comment has been updated
            if comment.timestamp == comment.last_edited:
                comment_data['last_edited'] = None
            else:
                comment_data['last_edited'] = comment.last_edited.isoformat()

            comments_data.append(comment_data)

        if comments_data:
            return {'status': 'success', 'data': comments_data}, 200
        
        else:
            return {'status': 'fail', 'message': 'Post not found'}, 404



    @jwt_required()
    def post(self, post_id):
        current_user = get_jwt_identity()

        # Parse the comment data from the request 
        data = json.loads(request.form['data'])
        content = data.get('content')

        # check if content isn't empty.
        if not content:
            return {'status': 'fail', 'message':'Content should not be empty !!'}
        
        # get the post to add the comment to. 
        post = Post.query.get_or_404(post_id)

        # get the comment itself. 
        comment = Comment(content=content, user_id=current_user, post_id=post_id)

        # add the comment to the database 
        db.session.add(comment)
        db.session.commit()

        # invalidate the cache.
        cache.delete(f"comment_data_{current_user}")

        return {'status': 'success', 'message': 'Comment added successfully !!', 'data': {'id': comment.id, 'content': comment.content}}, 201
    

    @jwt_required()
    def put(self, post_id, comment_id):
        current_user = get_jwt_identity()

        # Parse the comment data from the request
        data = json.loads(request.form['data'])
        content = data.get('content')

        # check if content isn't empty.
        if not content:
            return {'status': 'fail', 'message': 'Content should not be empty !!'}

        # get the comment to edit.
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id, user_id=current_user).first()

        if not comment:
            return {'status': 'fail', 'message': 'Comment not found or unauthorized to edit !!'}, 404

        # Update the comment content and commit to database
        comment.content = content if content else comment.content
        db.session.commit()

        # invalidate the cache.
        cache.delete(f"comment_data_{current_user}")

        return {'status': 'success', 'message': 'Comment updated successfully !!', 'data': {'id': comment.id, 'content': comment.content}}
    

    @jwt_required()
    def delete(self, post_id, comment_id):
        current_user_id = get_jwt_identity()

        # get the comment to be deleted. 
        comment = Comment.query.filter_by(id=comment_id, post_id=post_id).first()

        # check if the comment exists
        if not comment:
            return {'status': 'fail', 'message': 'Comment does not exist !!'}, 404

        # check if the user is authorized to delete the comment
        if comment.user_id != current_user_id:
            return {'status': 'fail', 'message': 'You are not authorized to delete this comment !!'}, 403

        db.session.delete(comment)
        db.session.commit()

        # invalidate the cache.
        cache.delete(f"comment_data_{current_user_id}")

        return {'status': 'success', 'message': 'Comment deleted !!'}, 200
