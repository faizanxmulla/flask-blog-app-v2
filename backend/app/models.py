from flask import flash
from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email

import datetime
from datetime import datetime
from pytz import timezone

#---------------------------------------------------------------------------------

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy()

# ------------------------------


UserRoles = db.Table('UserRoles',
                    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, default='')
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    profile_image = db.Column(db.String(128), default='backend/static/profile/def.jpg')

    roles = db.relationship('Role', secondary=UserRoles,
                            backref=db.backref('users', lazy='dynamic'))

    posts = db.relationship('Post', back_populates='user', lazy='subquery', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    # token-based authentication
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # <-- MIGUEL GRINBERG --> 
    followers = db.relationship('Follow',
                            foreign_keys='Follow.followed_id',
                            backref=db.backref('followed', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')

    following = db.relationship('Follow',
                            foreign_keys='Follow.follower_id',
                            backref=db.backref('follower', lazy='joined'),
                            lazy='dynamic',
                            cascade='all, delete-orphan')

    # <-------------------->

    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def is_valid_email(email):
        return validate_email(email)

    def set_email(self, email):
        if not self.is_valid_email(email):
            raise ValueError('Invalid email address')
            flash('Invalid email address !!', 'danger')
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def total_posts_count(self):
        return db.session.query(Post).filter_by(user_id=self.id).count()

    def is_following(self, user):
        return self.following.filter(Follow.followed_id == user.id).count() > 0
    
    def follow(self, user):
        if not self.is_following(user):
            existing_follow = Follow.query.filter_by(follower_id=self.id, followed_id=user.id).first()

            if not existing_follow:
                new_follow = Follow(follower_id=self.id, followed_id=user.id)

                db.session.add(new_follow)
                user.follower_count += 1
                self.following_count += 1
                db.session.commit()

            flash('User is already following this user !! ', 'danger')


    def unfollow(self, user):
        if self.is_following(user):
            existing_follow = Follow.query.filter_by(follower_id=self.id, followed_id=user.id).first()
            
            if existing_follow:
                db.session.delete(existing_follow)
                user.follower_count -= 1
                self.following_count -= 1
                db.session.commit()

            flash('You are not following this user !!', 'danger')


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image,
            'followers': [user.to_dict() for user in self.followers],
            'following': [user.to_dict() for user in self.following]
        }

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.profile_image}')"



class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(128))

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Kolkata')))
    last_updated = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Kolkata')), onupdate=datetime.now(timezone('Asia/Kolkata')))

    status = db.Column(db.String(20))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='posts', lazy=True)

    comments = db.relationship('Comment', backref='posts', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.timestamp}')"



class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Kolkata')))
    last_edited = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Kolkata')), onupdate=datetime.now(timezone('Asia/Kolkata')))

    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.timestamp}')"



class Follow(db.Model):
    __tablename__ = 'follow'

    __table_args__ = (db.UniqueConstraint('follower_id', 'followed_id', name='uniq_constraint_follow'),)

    id = db.Column(db.Integer, primary_key=True)

    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Kolkata')))

    def __repr__(self):
        return f"Follow(follower_id={self.follower_id}, followed_id={self.followed_id}, timestamp='{self.timestamp}')"