import unittest
from app import create_app, db
from app.models import Role, User, Permission, AnonymousUser

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.create_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password="lius")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="lius")
        with self.assertRaises(AttributeError):#####
            u.password

    def test_password_verify(self):
        u = User(password="lius")
        self.assertTrue(u.verify_password(password="lius"))
        self.assertFalse(u.verify_password(password="alex"))

    def test_roles_and_permissions(self):
        u = User(username="lius", password="123")
        self.assertTrue(u.can(Permission.WRITE))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))