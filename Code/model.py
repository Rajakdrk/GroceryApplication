from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Admin_login(db.Model):
    a_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)#change password as password

class User_login(db.Model):
    u_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)#change password as password
    cart_items = db.relationship('Cart_items')
    orders = db.relationship('Orders')

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref="categories", secondary="association")

class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    manufacturing_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity_type = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer(), nullable=False) #integer or decimal
    imageId = db.Column(db.Integer(), db.ForeignKey('image.id'), nullable=False)
    total_no_of_products = db.Column(db.Integer(), nullable=False) #total no.of products available in the store
    
class Cart_items(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pid = db.Column(db.Integer(), nullable=False)
    u_id = db.Column(db.Integer(), db.ForeignKey('user_login.u_id'), nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    u_id = db.Column(db.Integer(), db.ForeignKey('user_login.u_id'), nullable=False)
    pid = db.Column(db.Integer(), nullable=False)
    no_of_products = db.Column(db.Integer(), nullable=False)
    totalCost = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(), nullable=False)

#association between category and product relation many to many
class Association(db.Model):
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"), primary_key=True)
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), primary_key=True)

class Image(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    # pid = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True, nullable=False)
    products = db.relationship('Product')