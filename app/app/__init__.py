from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True , nullable = False)
	email = db.Column(db.String(120), unique = True , nullable = False)
	image_file = db.Column(db.String(20),nullable = False, default= 'default.png')
	password = db.Column(db.String(60),nullable=False)
	post = db.relationship('Post',backref='author',lazy = True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"

db.create_all()
#app._static_folder = os.path.abspath('static/')
#print(app.root_path)
from app import views
from app import admin_views
from app import jinjax
#from app import jinja2_templates
