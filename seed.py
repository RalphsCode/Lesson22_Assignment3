"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

# If table isn't empty, empty it
with app.app_context():
    User.query.delete()
    Post.query.delete()

# Add Users
ima = User(first_name='Ima', last_name="Genius", image_url="https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png")  # 553 is male
crystal = User(first_name="Crystal", last_name="ball", image_url="https://cdn.pixabay.com/photo/2014/04/02/17/07/user-307993_1280.png")  # 993 is female
robin = User(first_name='Robin', last_name="Banks", image_url="https://cdn.pixabay.com/photo/2014/04/02/17/07/user-307993_1280.png")
will = User(first_name='Will', last_name="Power", image_url="https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png")  

# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add_all([ima, crystal, robin, will]) 

    # Commit--otherwise, this never gets saved!
    db.session.commit()

# Add Posts
a = Post(title="My First Post", content="Ok, so this cat walks into a bar...", user_id=1)
b = Post(title="Never Gets Old", content="Coding is so much fun, it never gets old. I do though, cuz it takes me so long to write the code!", user_id=1)
c = Post(title="Going to work tonite", content="You'll prolly hear about it in the morning!", user_id=3)

# Add new objects to session, so they'll persist
with app.app_context():
    db.session.add_all([a,b,c]) 

    # Commit--otherwise, this never gets saved!
    db.session.commit()

# Add Tags
t1 = Tag(name="joke")
t2 = Tag(name="coding")
t3 = Tag(name="work")

with app.app_context():
    db.session.add_all([t1, t2, t3])
    db.session.commit()