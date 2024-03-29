from bookbits import db, login_manager
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    surname = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    about = db.Column(db.String, default="")
    title = db.Column(db.String, default="")
    image_file = db.Column(db.String(20), default='default_avatar.jpg')
    cover_photo = db.Column(db.String, default='default_cover.jpg')
    posts = db.relationship('Posts', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='com_author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_email = db.Column(db.String)
    sender_name = db.Column(db.String)
    reciever = db.Column(db.String)
    title = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    message_text = db.Column(db.Text)


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, default=datetime.now())
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    com_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

