from flask import Flask,render_template,redirect, request,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
#app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files
app.config['SECRET_KEY'] = "random string"

# Initialize Flask-Session
#Session(app)


db = SQLAlchemy(app) #connection



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100)) # hashed
    role = db.Column(db.String(100)) # admin or staff


'''
def __init__(self,email,password_hash):
     self.email = email
     self.password_hash = password_hash
     #self.role = role
'''



class MenuItems(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    category = db.Column(db.String(100))

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id")) # forgein key to Users
    total_price = db.Column(db.Float) # total order cost
    created_at = db.Column(db.String(100)) # datetime order timestamp

class OrderItems(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey("orders.id")) #forgein key to Orders
    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_items.id")) # forgein key to Menuitems
    quantity =db.Column(db.Integer)



with app.app_context():
    db.create_all()
    print("Database and tables are created")





@app.route("/")
def index():
    # If no username in session, redirect to login
    if not session.get("name"):
        return redirect("/login")
    return render_template("login.html")


@app.route("/login", methods = ['POST', 'GET'])
def login():
     
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        login = User.query.filter_by(email=email, password=password).first()
        
        if login is not None:
            print("login success")
            session["user_id"] = login.id
            session["role"] = login.role
            return redirect(url_for("dashboard"))
        else:
            print("login failed")
    return render_template("login.html")

'''
     if request.method == 'POST':
         if not request.form['email'] or not request.form['password']:
             print("failed")
         else:
             print("success")#tUser= User(request.form['email'], request.form['password'])
'''
       


    

@app.route("/menu")
def menu():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("menu.html")

@app.route("/orders")
def orders():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("orders.html")

# changes depnding on the role
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    print("LOGOUT HIT")
    session.clear()
    return redirect(url_for("login"))

@app.route("/manage_user")
def manage_user():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get('role') == 'admin':
        return render_template("manage_user.html")
    return redirect(url_for("dashboard"))



@app.route("/create_user")
def create_user():
    user = User(email="test@test.com", password="123", role="admin")
    user = User(email="staff@test.com", password="123", role="staff")
    db.session.add(user)
    db.session.commit()
    return "User created"


if __name__ == "__main__":
    app.run(debug=True)