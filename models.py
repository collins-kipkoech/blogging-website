
from datetime import datetime
from __main__ import db

class User(db.Model):
    """
    id, username, email, password, image_file, posts
    """
    

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    image_file = db.Column(db.String(50),nullable=False,default='avatar.jpg')
    password = db.Column(db.String(20),nullable=False)
   
    posts = db.relationship('Post',backref='author',lazy=True)


    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    """
    id, title, content, date_posted, user_id
    """
    

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"