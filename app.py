"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'our-secret-key'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def index():
    return redirect("/users")
    
@app.route("/users")
def users_list():
    users = User.query.all()
    return render_template('user_listing.html',users=users)

@app.route("/users/new")
def new_user_form():
    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def new_users():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    profile_url = request.form['profile_url']
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=profile_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    name = f"{user.first_name} {user.last_name}"
    url = user.image_url
    return render_template("user_detail.html", name=name, url=url, id=user_id)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)
