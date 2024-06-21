from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ponderosa@localhost/blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Turn off Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Remove all tables from the database
with app.app_context():
    db.drop_all()
    # Create all tables from the Models
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            User.query.delete()
            user = User(first_name="Testy", last_name="McTester", image_url='https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png')
            post = Post(title="Test Post", content="A test post for unitTesting.", user_id="1")
            db.session.add(user)
            db.session.add(post)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_user(self):
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("User Details", html)

    def test_user_edit(self):
        with app.test_client() as client:
            resp = client.get("/users/1/edit")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Update", html)

    def test_post(self):
        with app.test_client() as client:
            resp = client.get("/posts/1")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Post", html)
