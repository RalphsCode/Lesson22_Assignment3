"""Models for Blogly."""

import datetime

# File to handle the DB connections.
from flask_sqlalchemy import SQLAlchemy

# Connect Flask with SQLAlchemy
db = SQLAlchemy()  		# create variable to run SQLAlchemy / connect to database

#Put the connection in a function so it doesn't run immediately and unnecessarily.
def connect_db(app):
        db.app = app  			# associate flask app with the db variable
        db.init_app(app)   		# initialize

# models go below

class User(db.Model):
        """Class for Users"""

        __tablename__ = 'users'

        def __repr__(self):
                return f"<User id={self.id} - {self.first_name} {self.last_name} - {self.user_posts}>"

        id = db.Column(db.Integer,    # Create int column called id
                   primary_key=True,
                   autoincrement=True)

        first_name = db.Column(db.String(50),  # Create name column
                     nullable=False)

        last_name = db.Column(db.String(50),  # Create name column
                     nullable=False)

        image_url = db.Column(db.String(250),  # Create column to store the image URL
                     default='none',
                     nullable=True)
        
        user_posts = db.relationship('Post', backref='user')
             
class Post(db.Model):
        """Class for User's posts"""

        __tablename__ = 'posts'

        def __repr__(self):
                return f"<{self.title} - {self.user_id}>"

        id = db.Column(db.Integer,    # Create int column called id
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
        