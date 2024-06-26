"""Models for Blogly."""

import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  		

#Put the connection in a function so it doesn't run immediately and unnecessarily.
def connect_db(app):
        db.app = app  			# associate flask app with the db variable
        db.init_app(app)   		# initialize

#### MODELS BELOW ####

class User(db.Model):
        """Class for Blogly Users"""

        __tablename__ = 'users'

        # Better description
        def __repr__(self):
                return f"<User id={self.id} - {self.first_name} {self.last_name} - {self.user_posts}>"

        id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

        first_name = db.Column(db.String(50),
                     nullable=False)

        last_name = db.Column(db.String(50),
                     nullable=False)

        image_url = db.Column(db.String(250),
                     default='none',
                     nullable=True)
        
        # Create a relationship between Post and user
        user_posts = db.relationship('Post', backref='user', cascade="all, delete")
             
class Post(db.Model):
        """Class for User's posts"""

        __tablename__ = 'posts'

        def __repr__(self):
                return f"<{self.title} - {self.user_id} >"

        id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
        
        title = db.Column(db.Text, 
                          nullable=False)
        
        content = db.Column(db.Text,
                            nullable=False)
        
        created_at = db.Column(
                        db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
        
        user_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False)
        

class Tag(db.Model):
        """Class for Tagging User's posts"""

        __tablename__ = 'tags'

        def __repr__(self):
                return f"<{self.id} - {self.name}>"

        id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
        
        name = db.Column(db.Text,
                         nullable=False)
        
        # Create a relationship between post and post_tags
        posts = db.relationship('Post',
                               secondary='post_tags',
                               backref='post_tags', cascade="all, delete")
        

class PostTag(db.Model):
        """ Association Table, Class for joining users tags & posts"""

        __tablename__ = 'post_tags'

        post_id = db.Column(db.Integer,
                   db.ForeignKey('posts.id', ondelete="CASCADE"),
                   primary_key=True)
        
        tag_id = db.Column(db.Integer,
                   db.ForeignKey('tags.id', ondelete="CASCADE"),
                   primary_key=True)
        
        tag_info = db.relationship('Tag')