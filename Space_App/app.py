from crypt import methods
from distutils.log import error
import os
import requests
import json


from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, UserEditForm
from models import db, connect_db, User, Role
from secret import secretNASA

CURR_USER_KEY = "current_user"
app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///spacetracker'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "nerea")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# Home Page


@app.route('/')
def home():
    """Home Page"""

    return render_template('home.html')


##############################################################################
# News Page


@app.route('/news')
def news():
    """News Page
    Shows the 5 most recent space news from the spaceflightnews API
    """

    # Get space news
    url = "https://api.spaceflightnewsapi.net/v3/articles?_limit=5"
    response = requests.get(url)
    if response:
        response = response.json()
    else:
        flash("Something went wrong...try again later!", error)

    return render_template('news.html', response=response)


##############################################################################
# Launches Page


@app.route('/launches')
def launches():
    """Launches Page
    Shows the next five launches from rocketLaunch.Live API
    """

    # Get launches
    url = "https://fdo.rocketlaunch.live/json/launches/next/5"
    response = requests.get(url)
    if response:
        response = response.json()
    else:
        flash("Something went wrong...try again later!", error)

    return render_template('launches.html', response=response)


##############################################################################
# Image of the Day Page


@app.route('/potd')
def picture():
    """POTD Page
    Shows NASA Picture of The Day
    """

    # Get image
    url = 'https://api.nasa.gov/planetary/apod?api_key=%s' % secretNASA
    response = requests.get(url)
    if response:
        response = response.json()
    else:
        flash("Something went wrong...try again later!", error)

    return render_template('image.html', response=response)

##############################################################################
# User signup/login/logout

# Session and Flask Global Management before each request


@app.before_request
# the function add_user_to_g is executed before every function
# g stands for "global" and is an global namespace object in Flask. Only valid in the context and disappear when the context end.  Do not store data you need across requests (in this case, use session)
# A new request will end the context. This is why the following function needs to be done before each request and access the session to get the current user.
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


# Signup Route
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


# # Login Route
# @app.route('/login', methods=["GET", "POST"])
# def login():
#     """Handle user login."""

#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.authenticate(form.username.data,
#                                  form.password.data)

#         if user:
#             do_login(user)
#             flash(f"Hello, {user.username}!", "success")
#             return redirect("/")

#         flash("Invalid credentials.", 'danger')

#     return render_template('users/login.html', form=form)


# # Logout Route
# @app.route('/logout')
# def logout():
#     """Handle logout of user."""

#     user = User.query.get_or_404(session[CURR_USER_KEY])
#     # can also use g
#     #user = g.user
#     flash(f"See you later, {user.username}!")

#     do_logout()

#     return redirect("/login")
