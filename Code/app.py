from flask import Flask, render_template, request, redirect, url_for
from model import *
from datetime import datetime

# ================================ Configaration starts ================================
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Model.db"
db.init_app(app)
app.app_context().push()
db.create_all()
# ================================= Configaration ends =================================


# ================================= Controller starts ===================================
@app.route('/', methods = ['GET', 'POST'])
def Hello():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)

# ===================  admin  ======================
@app.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("adminLoginForm.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admins = Admin_login.query.all()
        categories = Category.query.all()
        products = Product.query.all()
        flag = True
        for admin in admins:
            if admin.username == username and admin.password == password:
                flag = False
                return redirect(url_for("admin_dashboard", username=username, categories=categories, products=products))
        if flag:
            return render_template("errorPage.html")
    
@app.route('/admin_dashboard/<username>', methods = ['GET', 'POST'])
def admin_dashboard(username):
    categories = Category.query.all()
    products = Product.query.all()
    db.session.commit()
    return render_template("adminDashboard.html", username=username, categories=categories, products=products)

@app.route('/addCategory/<username>', methods=['GET', 'POST'])
def addCategory(username):
    admins = Admin_login.query.all()
    if request.method == 'GET':
        return render_template("addCategory.html", username=username)
    elif request.method == 'POST':
        addCategory = request.form.get('categoryName')
        category = Category(name=addCategory)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin_dashboard", username=username))

@app.route('/deleteCategory/<username>/<int:id>', methods = ['GET', 'POST'])
def deleteCategory(username, id):
    category = Category.query.get(id)
    category.products.clear()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("admin_dashboard", username=username))

@app.route('/editCategory/<username>/<int:id>', methods = ['GET', 'POST'])
def editCategory(username, id):
    if request.method == 'GET':
        category = Category.query.get(id)
        return render_template("editCategory.html", username=username, category=category)
    elif request.method == 'POST':
        category = Category.query.get(id)
        categoryName = request.form.get('categoryName')
        category.name = categoryName
        db.session.commit()
        return redirect(url_for("admin_dashboard", username=username))

@app.route('/addProductToCategory/<username>/<int:id>', methods = ['GET', 'POST'])
def addProductToCategory(username, id):
    if request.method == 'GET':
        category = Category.query.get(id)
        categoryName = category.name
        products = Product.query.all()
        return render_template("addProductToCategory.html", products=products, categoryName=categoryName, id=id)
    elif request.method == 'POST':
        productID = int(request.form.get('product'))    
        product = Product.query.get(productID)
        category = Category.query.get(id)
        category.products.append(product)
        db.session.commit()
        return redirect(url_for("admin_dashboard", username=username))

@app.route('/editProduct/<username>/<int:id>', methods = ['GET', 'POST'])
def editProduct(username, id):
    if request.method == 'GET':
        product = Product.query.get(id)
        return render_template("editProduct.html", username=username, product=product)
    elif request.method == 'POST':
        product = Product.query.get(id)
        productName = request.form.get('productName')
        expiryDate = request.form.get('expiryDate')
        year, month, day = expiryDate.split('-')
        quantityType = request.form.get('quantityType')
        price = request.form.get('price')
        product.name = productName
        product.expiry_date = datetime(int(year), int(month), int(day))
        product.quantity_type = quantityType
        product.price = price
        db.session.commit()
        return redirect(url_for("admin_dashboard", username=username))

@app.route('/deleteProduct/<username>/<int:cid>/<int:pid>', methods = ['GET', 'POST'])
def deleteProduct(username, cid, pid):
    category = Category.query.get(cid)
    product = Product.query.get(pid)
    category.products.remove(product)
    db.session.commit()
    return redirect(url_for("admin_dashboard", username=username))

@app.route('/editAllProductsFromDB/<username>', methods = ['GET', 'POST'])
def editAllProductsFromDB(username):
    if request.method == 'GET':
        products = Product.query.all()
        return render_template("editAllProductsFromDB.html", username=username, products=products)

@app.route('/deleteProduct/<username>/<int:pid>', methods = ['GET', 'POST'])
def deleteProductss(username, pid):
    if request.method == 'GET':
        product = Product.query.get(pid)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('editAllProductsFromDB', username=username))

@app.route('/addProduct/<username>', methods = ['GET', 'POST'])
def addProduct(username):
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template("addProduct.html", username=username, categories=categories)
    elif request.method == 'POST':
        productName = request.form.get('productName')
        expiryDate = request.form.get('expiryDate')
        year, month, day = expiryDate.split('-')
        quantityType = request.form.get('quantityType')
        price = request.form.get('price')
        product = Product(name=productName, expiry_date=datetime(int(year), int(month), int(day)), quantity_type=quantityType, price=price)
        db.session.add(product)
        category = request.form.get('category')
        if(category != "none"):
            thisCategory = Category.query.get(category)
            product.categories.append(thisCategory)
        db.session.commit()
        return redirect(url_for('editAllProductsFromDB', username=username))
# ===================  admin  ======================



# ===================  user  ======================
@app.route('/user_login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template("UserLoginForm.html")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User_login.query.all()
        flag = True
        for user in users:
            if user.username == username and user.password == password:
                flag = False
                return redirect(url_for("user_dashboard", username=username))
        if flag:
            return render_template("errorPage.html")

@app.route('/user_dashboard/<username>', methods = ['GET', 'POST'])
def user_dashboard(username):
    return render_template("userDashboard.html", username=username)

@app.route('/user_registration', methods = ['GET', 'POST'])
def user_registration():
    return render_template("userRegistration.html")
# ===================  user  =======================


# ================================= Controller ends ===================================


if __name__ == "__main__":
    app.run(debug=True)