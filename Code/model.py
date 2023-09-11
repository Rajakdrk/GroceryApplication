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
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref="categories", secondary="association")

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity_type = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer(), nullable=False) #integer or decimal
    
class Item_cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
class Association(db.Model):
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), primary_key=True)