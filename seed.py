"""Seed file to make sample data for pets db."""

from models import User, db, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add pets
Alan = User(first_name='Alan', last_name='Alda', image_url="https://i.insider.com/5cdecf14021b4c0e0d0514c5?width=1100&format=jpeg&auto=webp")
Joel = User(first_name='Joel', last_name='Burton', image_url="https://cf.ltkcdn.net/cats/images/std/235591-1600x1067-grumpy-cat.jpg")
Jane = User(first_name='Jane', last_name='Smith', image_url="https://static.themoscowtimes.com/image/1360/4e/26.jpg")

# Add posts
Post1 = Post(title="My first post", content="Wow this is so fun", user_id=1)
Post2 = Post(title="FLASK FUN", content="flask so cool", user_id=2)
Post3 = Post(title="Cats are cool", content="grumpy cat is a cool cat", user_id=3)
# Add new objects to session, so they'll persist
db.session.add(Alan)
db.session.add(Joel)
db.session.add(Jane)
db.session.add(Post1)
db.session.add(Post2)
db.session.add(Post3)
# Commit--otherwise, this never gets saved!
db.session.commit()