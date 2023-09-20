from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # this the id of each line on my sql tible, and it start from 1
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    # evry user have some post , so this line related the table post with the table user, and show 
    # what's from the table post are his personal post
    posts = db.relationship('Post', backref='author',lazy=True)

    def __repr__(self) -> str:
        return f"user('{self.username}' , '{self.email}' , '{self.image_file}')"
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    date_post = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # this line is relate the table post with user, that ecry post have one user or author can be writing
    # and for that we pot for eatch post user_id of author
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"user('{self.title} , {self.date_post}')"