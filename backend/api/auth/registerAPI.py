import secrets
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse

from app.models import db, User

# --------------------------------------------------------------------------------

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username is required !!')
parser.add_argument('email', type=str, required=True, help='Email is required !!')
parser.add_argument('password', type=str, required=True, help='Password is required !!')


class RegisterAPI(Resource):
    def post(self):
        args = parser.parse_args()
        username = args.get('username')
        email = args.get('email')
        password_hash = args.get('password')

        # check if the username is already registered or the username is already taken
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return {'message': 'Username already registered !!'}

        # Create a new user object and set their password
        hashed_password = hash_password(password_hash)

        new_user = User(username=username, email=email, password_hash= hashed_password)

        new_user.fs_uniquifier = secrets.token_hex(16)

        # Add the user object to the database and commit the changes
        db.session.add(new_user)
        db.session.commit()

        return {'status': 'success','message': 'Successfully Registered !!'}
