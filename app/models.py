from datetime import datetime
from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import jwt
from time import time

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	comments = db.relationship("Comment", foreign_keys="Comment.user_id", backref="user",lazy="dynamic")
	like = db.relationship("Postlike", foreign_keys="Postlike.user_id",backref="user", lazy="dynamic")

	def like_post(self,post):
		if not self.has_liked_post(post):
			liked = Postlike(user_id=self.id,post_id=post.id)
			db.session.add(liked)

	def comment_post(self,post,body):
		commented = Comment(user_id=self.id,post_id=post.id,body=body)
		db.session.add(commented)

	def unlike_post(self,post):
		if self.has_liked_post(post):
			print("yes")
			Postlike.query.filter(Postlike.user_id==self.id,Postlike.post_id==post.id).delete()

	def uncomment_post(self,post):
		if self.has_commented_post(post):
			Comment.query.filter(Comment.user_id==self.id,Comment.post_id==post_id).delete()

	def has_liked_post(self,post):
		return Postlike.query.filter(
			Postlike.user_id==self.id,
			Postlike.post_id==post.id).count()>0

	def has_commented_post(self,post):
		return Comment.query.filter(
			Comment.user_id==self.id,
			Comment.post_id==post.id).count()>0

	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(
			followers.c.followed_id == user.id).count() > 0	

	def followed_posts(self):
		followed = Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.timestamp.desc())

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
	
	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	tag = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	likes = db.relationship("Postlike", backref="post",lazy="dynamic")
	comments = db.relationship("Comment", backref="post",lazy="dynamic")

	def __repr__(self):
		return '<Post {}>'.format(self.body)

class Postlike(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
	post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
		
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
	post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


