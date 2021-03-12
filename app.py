"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    users = User.query.order_by('first_name').all()
    
    return render_template('user_listing.html',users=users)

@app.route("/users/new")
def new_user_form():
    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def process_new_user():
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
    posts = user.posts
    name = f"{user.first_name} {user.last_name}"
    url = user.image_url
    return render_template("user_detail.html", name=name, url=url, id=user_id, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["profile_url"]
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    name = f"{user.first_name} {user.last_name}"
    return render_template("new_post_form.html", user=user, name=name)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def process_post_form(user_id):
    title = request.form["post-title"]
    content = request.form["post-content"]
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def user_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def process_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["post-title"]
    post.content = request.form["post-content"]
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.author.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")