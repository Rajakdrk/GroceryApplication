from flask import Flask, render_template, request, redirect, url_for
from model import *
from datetime import datetime
from werkzeug.utils import secure_filename
import base64

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
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str, image.name])
    return render_template("index.html", categories=categories, images=images)

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
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str])
    categories = Category.query.all()
    products = Product.query.all()
    db.session.commit()
    return render_template("adminDashboard.html", images=images, username=username, categories=categories, products=products)

@app.route('/addCategory/<username>', methods=['GET', 'POST'])
def addCategory(username):
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
        imagesFromDB = Image.query.all()
        images = []
        for image in imagesFromDB:
            imageData = image.img
            plain_str = base64.b64encode(imageData).decode("utf-8")
            images.append([image.id, plain_str])
        return render_template("editAllProductsFromDB.html", images=images, username=username, products=products)

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
        images = Image.query.all()
        categories = Category.query.all()
        return render_template("addProduct.html", username=username, categories=categories, images=images)
    elif request.method == 'POST':
        productName = request.form.get('productName')
        manufacturingDate = request.form.get('expiryDate')
        Myear, Mmonth, Mday = manufacturingDate.split('-')
        expiryDate = request.form.get('expiryDate')
        year, month, day = expiryDate.split('-')
        quantityType = request.form.get('quantityType')
        price = request.form.get('price')
        imageId = request.form.get('productImage')
        totalNoOfProducts = request.form.get('totalNoOfProducts')
        product = Product(name=productName, manufacturing_date=datetime(int(Myear), int(Mmonth), int(Mday)), expiry_date=datetime(int(year), int(month), int(day)), quantity_type=quantityType, price=price, imageId=imageId, total_no_of_products=totalNoOfProducts)
        db.session.add(product)
        category = request.form.get('category')
        if(category != "none"):
            thisCategory = Category.query.get(category)
            product.categories.append(thisCategory)
        db.session.commit()
        return redirect(url_for('editAllProductsFromDB', username=username))
    
#uploading images for Product
@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload(username):
    if request.method == 'GET':
        return render_template("uploadProductImage.html", username=username)
    elif request.method == 'POST':
        image = request.files['productImage']
        if not image:
            return "<h1>No Image..!</h1>"
        filename = secure_filename(image.filename)
        mimetype = image.mimetype
        img = Image(img=image.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        return redirect(url_for('addProduct', username=username))

# To see all Product image in DB
@app.route('/seeImages/<username>', methods=['GET', 'POST'])
def seeImages(username):
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str, image.name])
    return render_template('seeImagesInDB.html', username=username, images=images)
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
    categories = Category.query.all()
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str, image.name])
    return render_template("userDashboard.html", images=images, username=username, categories=categories)

@app.route('/user_registration', methods = ['GET', 'POST'])
def user_registration():
    if request.method == 'GET':
        return render_template("userRegistration.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #checking username is unique or not
        try:
            user = User_login(username=username, password=password)
            db.session.add(user)
            db.session.commit()
        except:
            return render_template("errorPage.html")
        return redirect(url_for("user_dashboard", username=username))
    
@app.route('/search/category/<username>', methods = ['GET', 'POST'])
def search(username):
    if request.method == 'POST':
        
        imagesFromDB = Image.query.all()
        images = []
        for image in imagesFromDB:
            imageData = image.img
            plain_str = base64.b64encode(imageData).decode("utf-8")
            images.append([image.id, plain_str, image.name])

        searchCategoryName = request.form.get('search')
        #all Categories contains similar to search
        categories = Category.query.filter(Category.name.icontains(searchCategoryName)).all()
        return render_template("userDashboard.html", username=username, categories=categories, images=images)
        
@app.route('/search/product/<username>', methods = ['GET', 'POST'])
def searchProduct(username):
    if request.method == 'POST':
        imagesFromDB = Image.query.all()
        images = []
        for image in imagesFromDB:
            imageData = image.img
            plain_str = base64.b64encode(imageData).decode("utf-8")
            images.append([image.id, plain_str, image.name])

        searchProductName = request.form.get('search')
        products = Product.query.filter(Product.name.icontains(searchProductName) | Product.price.icontains(searchProductName)).all()
        return render_template("searchProducts.html", username=username, products=products, images=images)

@app.route('/cart/<username>', methods = ['GET', 'POST'])
def cart(username):
    user = User_login.query.filter(User_login.username.icontains(username)).first()
    productsINCart = user.cart_items
    products = []
    for item in productsINCart:
        product = Product.query.get(item.pid)
        products.append(product)
    #all images in the form of base64
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str, image.name])
    return render_template("cart_items.html", username=username, products=products, images=images)

@app.route('/addProductToCart/<username>/<int:pid>', methods = ['GET', 'POST'])
def addProductToCart(username, pid):
    u_id = User_login.query.filter(User_login.username.icontains(username)).first().u_id
    cart = Cart_items(pid=pid, u_id=u_id)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for("user_dashboard", username=username))

@app.route('/removeProductFromCart/<username>/<int:pid>', methods = ['GET', 'POST'])
def removeProductFromCart(username, pid):
    user = User_login.query.filter(User_login.username.icontains(username)).first()
    productsINCart = user.cart_items
    id = None
    for product in productsINCart:
        if product.pid == pid:
            id = product.id
            break
    cart = Cart_items.query.get(id)
    user.cart_items.remove(cart)
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for("user_dashboard", username=username))

@app.route('/yourOrders/<username>', methods = ['GET', 'POST'])
def yourOrders(username):
    user = User_login.query.filter(User_login.username.icontains(username)).first()
    orders = user.orders
    products = Product.query.all()
    imagesFromDB = Image.query.all()
    images = []
    for image in imagesFromDB:
        imageData = image.img
        plain_str = base64.b64encode(imageData).decode("utf-8")
        images.append([image.id, plain_str, image.name])
    return render_template("yourOrders.html", username=username, orders=orders, products=products, images=images)

#user BUYING the product
@app.route('/buy/<int:pid>/<username>', methods = ['GET', 'POST'])
def buy(pid, username):
    u_id = User_login.query.filter(User_login.username.icontains(username)).first().u_id
    if request.method == 'GET':
        return render_template("buy.html", username=username, pid=pid)
    elif request.method == 'POST':
        product = Product.query.get(pid)
        total_no_of_products = product.total_no_of_products

        #form data
        no_of_products = request.form.get('no_of_products')
        no_of_products = int(no_of_products)
        address = request.form.get('address')

        if total_no_of_products >= no_of_products:
            price = product.price
            totalCost = price*int(no_of_products)
            order = Orders(u_id=u_id, pid=pid, no_of_products=no_of_products, totalCost=totalCost, address=address)
            #change the no.of products in Products relation
            product.total_no_of_products = total_no_of_products-no_of_products
            db.session.add(order)
            db.session.commit()
            return redirect(url_for("yourOrders", username=username))
        elif total_no_of_products < no_of_products:
            return "<p>Choose less number of products || that no.of of products are not available...</p>"


@app.route('/buyAllProducts/<username>', methods = ['GET', 'POST'])
def buyAllProducts(username):
    user = User_login.query.filter(User_login.username.icontains(username)).first()
    u_id = User_login.query.filter(User_login.username.icontains(username)).first().u_id
    productsINCart = user.cart_items
    products = []
    for item in productsINCart:
        product = Product.query.get(item.pid)
        if product not in products:
            products.append(product)

    if request.method == 'GET':
        return render_template("buyAllProducts.html", username=username, products=products)
    elif request.method == 'POST':
        address = request.form.get('address')
        totalCost = 0
        for product in products:
            total_no_of_products = product.total_no_of_products
            noOfProducts = int(request.form.get(str(product.id)))
            if total_no_of_products >= noOfProducts:
                totalCostLocal = product.price*noOfProducts
                totalCost = totalCost+totalCostLocal
                order = Orders(u_id=u_id, pid=product.id, no_of_products=noOfProducts, totalCost=totalCostLocal, address=address)
                product.total_no_of_products = total_no_of_products-noOfProducts
                db.session.add(order)
            elif total_no_of_products < noOfProducts:
                return "<p>Choose less number of products || that no.of of products are not available...</p>"
        db.session.commit()
        print("total Cost.......", totalCost)
        return redirect(url_for("yourOrders", username=username))


@app.route('/totalCost/<username>', methods = ['GET'])
def totalCost(username):
    if request.method == 'GET':
        user = User_login.query.filter(User_login.username.icontains(username)).first()
        productsINCart = user.cart_items
        products = []
        for item in productsINCart:
            product = Product.query.get(item.pid)
            if product not in products:
                products.append(product)
        
        totalCost = 0
        for product in products:
            noOfProducts = int(request.form.get(str(product.id)))
            totalCostLocal = product.price*noOfProducts
            totalCost = totalCost+totalCostLocal

        return render_template("totalCost.html", username=username, products=products, totalCost=totalCost)
# ===================  user  =======================


# ================================= Controller ends ===================================


if __name__ == "__main__":
    app.run(debug=True)