"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)  # creating an instance of the Flask Class

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ponderosa@localhost/blogly'
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

with app.app_context():
    connect_db(app)
    db.create_all()

app.config['SECRET_KEY'] = "RalphsCode123"
debug = DebugToolbarExtension(app)

####### ROUTES #########

@app.route('/')
def home():
    # Display all Users and Link to View All Tags
    return redirect('/users')


@app.route('/users')
def users():
    # Display All Users
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    # Add a New User
    if request.method == 'GET':
        # Display the new user form
        return render_template('new_user.html')
    else:
        # Process the new user form
        first = request.form['first_name']
        last = request.form['last_name']
        img_url = request.form['image_url']
        new_user = User(first_name=first, last_name=last, image_url=img_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    # Display User Details
    user = User.query.get_or_404(user_id)
    post_titles = Post.query.filter_by(user_id = user_id).all()
    return render_template('user.html', user=user, post_titles=post_titles)


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    # Edit a User
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
        return render_template('edit_user.html', user=user)
    else:
        first_name = request.form.get('first_name')
        last_name  = request.form.get('last_name')
        image_url = request.form.get('image_url')
        # If 1 or more fields are updated, update the record
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if image_url != '':
            user.image_url = image_url
        flash('User has been updated')
        db.session.add(user)
        db.session.commit()
        return render_template('user.html', user=user)


@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    # Delete a User
    to_delete = User.query.get(user_id)
    # Delete any posts by the user to be deleted
    Post.query.filter_by(user_id=user_id).delete()
    # Delete the user
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    # Flash deleted user message
    flash(f'{to_delete.first_name} {to_delete.last_name} has been deleted')
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def add_post(user_id):
    # Create a New Post
    if request.method == 'GET':
        return render_template('new_post.html', user_id=user_id)
    else:
        new_title = request.form['title']                                   
        new_post = request.form['content']
        new_post = Post(title=new_title, content=new_post, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post Submitted')
        return redirect('/users')


@app.route('/posts/<int:post_id>')
def display_post(post_id):
    # Display a Post
    post = Post.query.get(post_id)
    return render_template('display_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    # Edit a Post
    post = Post.query.get(post_id)
    if request.method == 'GET':
        return render_template('edit_post.html', post=post)
    else:
        title = request.form.get('title')
        content  = request.form.get('content')
        # Update the record object as needed
        if title != '':
            post.title = title
        post.content = content
        # Update the database table record
        db.session.add(post)
        db.session.commit()
        flash('Post has been updated')
        return render_template('display_post.html', post=post)


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    # Delete the post
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('Post has been deleted')
    user_id = request.args['user_id']
    print('#############', user_id, '##############')
    return redirect(f'/users/{user_id}')


@app.route('/tags')
def tags():
    # Display all tags
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new', methods=['GET', 'POST'])
def new_tag():
    # Add a New Tag
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template('new_tag.html', tags=tags)
    else:
        tag_name = request.form.get('name')
        if tag_name != '':
            create_tag = Tag(name = tag_name)
            db.session.add(create_tag)
            db.session.commit()
            flash(f'{tag_name} has been added.')
            return redirect('/tags')
        else:
            flash('The new tag field cannot be blank.')
            return redirect('/tags/new')


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    # Show the details on a particular tag
    tag = Tag.query.get(tag_id)
    tag_posts = tag.posts
    return render_template('display_tag.html', tag=tag, tag_posts=tag_posts)


@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    # Edit a tag
    tag = Tag.query.get(tag_id)
    if request.method == 'GET':
        return render_template('edit_tag.html', tag=tag)
    else:
        tag.name = request.form['name']
        db.session.add(tag)
        db.session.commit()
        return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    # Delete a tag
    # Start by deleting the tag from all posts
    PostTag.query.filter_by(tag_id=tag_id).delete()
    db.session.commit()
    # Then delete the tag itself
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    flash('Tag has been deleted')
    return redirect('/tags')
