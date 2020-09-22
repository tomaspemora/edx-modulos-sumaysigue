from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
import os
from pdb import set_trace as bp
from random import randrange

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True , nullable = False)
	email = db.Column(db.String(120), unique = True , nullable = False)
	image_file = db.Column(db.String(20),nullable = False, default= 'default.png')
	password = db.Column(db.String(60),nullable=False)
	post = db.relationship('Post',backref='author',lazy = "dynamic")

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"
	
	@classmethod
	def get_or_create(cls, username, email):
		exists = db.session.query(User.username).filter_by(username=username).scalar() is not None
		exists2 = db.session.query(User.email).filter_by(email=email).scalar() is not None
		if exists and exists2:
			return db.session.query(User).filter_by(username=username, email=email).first()
		return cls(username=username, email=email)

class Worker(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50),nullable=False)
	charge = db.relationship('Charge')
	
	def __repr__(self):
		return f"Worker('{self.name}')"


class Charge(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50),nullable=False)

	def __repr__(self):
		return f"Charge('{self.name}')"

class Context(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	project = db.Column(db.String(50),nullable=False)
	subproject = db.Column(db.String(50),nullable=False)

	def __repr__(self):
		return f"Context('{self.project}','{self.subproject}')"

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(150),nullable=False)
	program = db.relationship('Context')
	designer = db.relationship('Worker')
	designer_date = db.Column(db.DateTime,nullable=False)
	programmer = db.relationship('Worker')
	programmer_date = db.Column(db.DateTime,nullable=False)
	archivo = db.Column(db.Text,nullable=True)

	def __repr__(self):
		return f"Task('{self.description}','{self.program}','{self.designer_date}','{self.programmer_date}','{self.archivo}',)"

	@classmethod
	def get_or_create(cls, id, description):
		exists = db.session.query(User.id).filter_by(username=username).scalar() is not None
		exists2 = db.session.query(User.email).filter_by(email=email).scalar() is not None
		if exists and exists2:
			return db.session.query(User).filter_by(username=username, email=email).first()
		return cls(username=username, email=email)



def create_db(db):
	db.create_all()
	return db
'''for i in range(0,1000):
		rn = randrange(0, 255)
		usr = User.get_or_create(username='tomito'+str(i)+str(rn), email='tomiaspemora'+str(i)+str(rn)+'@gmail.com')
		if usr not in db.session:
			db.session.add(User(username='tomito'+str(i)+str(rn), email='tomiaspemora'+str(i)+str(rn)+'@gmail.com',password='tomito1'+str(i)))
	db.session.commit()'''
	
