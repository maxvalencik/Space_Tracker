"""SQLAlchemy models for Space Tracker"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


###############################################
# User Model
class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    location = db.Column(
        db.Text,
        nullable=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    role_id = db.Column(
        db.Integer,
        db.ForeignKey('roles.id',
                      ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )

    roles = db.relationship('Role', backref='users')

    # followers = db.relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_being_followed_id == id),
    #     secondaryjoin=(Follows.user_following_id == id),
    # )

    # following = db.relationship(
    #     "User",
    #     secondary="follows",
    #     primaryjoin=(Follows.user_following_id == id),
    #     secondaryjoin=(Follows.user_being_followed_id == id),
    # )

    # likes = db.relationship(
    #     'Message',
    #     secondary="likes"
    # )

    #### Methods ####
    # def __repr__(self):
    #     return f"<User #{self.id}: {self.username}, {self.email}>"

    # def is_followed_by(self, other_user):
    #     """Is this user followed by `other_user`?"""

    #     found_user_list = [
    #         user for user in self.followers if user == other_user]
    #     return len(found_user_list) == 1

    # def is_following(self, other_user):
    #     """Is this user following `other_use`?"""

    #     found_user_list = [
    #         user for user in self.following if user == other_user]
    #     return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, name, location, email, password, role_id):
        """This is a class method (call it on the class, not an individual user.)
        Sign up user. Hashes password and adds user to system."""

        # Look for existing username
        user_name = cls.query.filter_by(username=username).first()

        # Look for existing email
        email_user = cls.query.filter_by(email=email).first()

        # If the username or email already exist, return false
        if user_name or email_user:
            return False

        # Otherwise add new user
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            name=name or None,
            location=location or None,
            email=email,
            password=hashed_pwd,
            role_id=role_id,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


###############################################
# Role Model
class Role(db.Model):
    """User role: only three possible"""
    __tablename__ = 'roles'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    roleType = db.Column(
        db.String(10),
        nullable=False,
    )

    definition = db.Column(
        db.Text,
        nullable=True,
    )


###############################################
# connect_db
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
