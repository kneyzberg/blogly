"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String,
                          default='')
    
    posts = db.relationship("Post")

    # repr for the Users
    def __repr__(self):
        s = self
        return f'user id {s.id} first name is {s.first_name} last is {s.last_name}'


class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False,
                           default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

    author = db.relationship("User")

    tags = db.relationship("Tag",
                           secondary="post_tags")
    

class Tag(db.Model):
    """Tag"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    
    posts = db.relationship("Post",
                            secondary="post_tags")
  
                              
class PostTag(db.Model):
    """Post_tag_matchup"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_ids = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True)
    
    