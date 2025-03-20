from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/dummy'
app.config['SECRET_KEY'] = 'your_secret_key'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(120), nullable=False)


class Category(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120), nullable=False)


class Product(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120), nullable=False)
    price = database.Column(database.Float, nullable=False)
    description = database.Column(database.String(120), nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=False)
    category = database.relationship('Category', backref=database.backref('products', lazy=True))

@app.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    database.session.add(new_user)
    database.session.commit()
    return jsonify({'message': 'User created successfully. Navigating to Login'}), 201

@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')
    is_user_exist = User.query.filter_by(username=username).first()
    if is_user_exist and bcrypt.check_password_hash(is_user_exist.password, password):
        app.config['USER_LOGGED_IN'] = True
        app.config['LOGGED_IN_USER'] = is_user_exist.username  
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials or user does not exist'}), 401


def create_tables():
    with app.app_context():
        database.create_all()

        if not User.query.first():
            hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
            user1 = User(username="admin", password=hashed_password)
            database.session.add(user1)
            database.session.commit()
        
        if not Category.query.first():
            electronics = Category(name="Electronics")
            clothing = Category(name="Clothing")

            database.session.add(electronics)
            database.session.add(clothing)
            database.session.commit()

        if not Product.query.first():
            product1 = Product(name="Boat Eardopes 141", price=1500, category_id=1, description="13mm driver with 48 hours battery life + 6 months warranty")
            product2 = Product(name="Oneplus Neckband Z2", price=2000, category_id=1, description="12mm driver with 60 hours battery life + 1 year warranty")
            product3 = Product(name="BeYoungShirt", price=899, category_id=2, description="Cotton fabric material also available in all sizes with 5 different colour")
            product4 = Product(name="Allen Solly Tshirt", price=1299, category_id=2, description="Brand new Tshirt with 8 different colours")
            database.session.add(product1)
            database.session.add(product2)
            database.session.add(product3)
            database.session.add(product4)
            database.session.commit()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
