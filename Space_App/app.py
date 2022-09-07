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
# clear flash messages
def clear_flash():
    """Clear exisitng flash messages"""
    session.pop('_flashes', None)


##############################################################################
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


##############################################################################
# do after login
def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


##############################################################################
# do after logout
def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


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
    clear_flash()

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
    clear_flash()

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
    clear_flash()

    # Get image
    url = 'https://api.nasa.gov/planetary/apod?api_key=%s' % secretNASA
    response = requests.get(url)
    if response:
        response = response.json()
    else:
        flash("Something went wrong...try again later!", error)

    return render_template('image.html', response=response)


##############################################################################
# Signup Route
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message and re-present form.
    """

    clear_flash()
    form = UserAddForm()

    if form.validate_on_submit():

        user = User.signup(
            username=form.username.data,
            name=form.name.data or None,
            location=form.location.data or None,
            email=form.email.data,
            password=form.password.data,
            role_id=form.role.data,
        )

        if not user:

            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        flash('Welcome %s' % user.username)
        db.session.commit()
        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


##############################################################################
# Login Route
@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    clear_flash()
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash("Welcome back %s" % user.username)
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


##############################################################################
# Logout Route
@app.route('/logout')
def logout():
    """Handle logout of user."""

    clear_flash()

    user = User.query.get_or_404(session[CURR_USER_KEY])
    # can also use g
    #user = g.user
    flash(f"See you later, {user.username}!")

    do_logout()

    return redirect("/")


##############################################################################
# Profile Route
@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    clear_flash()

    if not g.user:
        flash("You need to login to get there!", "danger")
        return redirect("/")

    # get the current user using g.
    user = g.user

    # Pre-Fill the form with user data
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data,
            user.name = form.name.data or None,
            user.location = form.location.data or None,
            user.email = form.email.data,
            user.password = form.password.data,
            user.role_id = form.role.data,

            db.session.commit()
            return redirect("/")

        flash("Wrong data! Try again!", 'danger')

    return render_template('edit.html', form=form, user_id=user.id)
