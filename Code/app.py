from flask import Flask, render_template, request, redirect, url_for
from model import *

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

@app.route('/addProduct/<username>', methods = ['GET', 'POST'])
def addProduct(username):
    if request.method == 'GET':
        return render_template("addProduct.html", username=username)
    elif request.method == 'POST':
        return redirect(url_for("admin_dastboard", username=username))
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