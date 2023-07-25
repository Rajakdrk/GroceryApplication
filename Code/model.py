from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin_login(db.Model):
    a_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

class User_login(db.Model):
    u_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

class Category(db.Model):
    c_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False) 

class Product(db.Model):
    p_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity_type = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer(), primary_key=True) #integer or decimal
    
