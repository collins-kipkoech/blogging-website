
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
 
from werkzeug.security import generate_password_hash,check_password_hash


@login_manager.user_loader
def load_user(user_id):
    """
    function to get a user by id
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    id, username, email, password, image_file, posts
    """
    
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    email = db.Column(db.String(255),unique=True)
    image_file = db.Column(db.String(255),default='avatar.jpg')
    password = db.Column(db.String(255))
   
    posts = db.relationship('Post',backref='author',lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password,password)
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
    posts = db.relationship('Comment',backref='comment',lazy='dynamic')
    

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)     
    text = db.Column(db.String(255),index = True)        
    post = db.Column(db.Integer,db.ForeignKey('post.id'))       
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


