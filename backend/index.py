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


class Cart(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)

class Review(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    rating = database.Column(database.Integer, nullable=False)
    comment = database.Column(database.String(500), nullable=True)
    user = database.relationship('User', backref='reviews', lazy=True)

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


@app.route('/logout', methods=['POST'])
def logout():
    app.config['USER_LOGGED_IN'] = False
    app.config['LOGGED_IN_USER'] = None
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/categories', methods=['GET'])
def get_Categories():
    if not app.config['USER_LOGGED_IN']:
        return jsonify({'message': 'You must be logged in to view categories.'}), 403
    allCategories = Category.query.all()
    return jsonify([{'id': category.id, 'name': category.name} for category in allCategories])


@app.route('/products/<int:category_id>', methods=['GET'])
def get_Products_By_Category(category_id):
    if not app.config['USER_LOGGED_IN']:
        return jsonify({'message': 'You must be logged in to view products.'}), 403
    
    productsByCategoryId = Product.query.filter_by(category_id=category_id).all()

    products_data = []
    for product in productsByCategoryId:
        reviewsByProductId = Review.query.filter_by(product_id=product.id).all()
        
        reviews_data = [{
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id,
            'username': review.user.username
        } for review in reviewsByProductId]

        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'reviews': reviews_data
        })

    return jsonify(products_data)


@app.route('/add_to_cart', methods=['POST'])
def add_To_Cart():

    if not app.config['USER_LOGGED_IN']:
        return jsonify({'message': 'You must be logged in to add items to the cart.'}), 403

    json_data = request.get_json()
    product_id = json_data.get('product_id')
    product_quantity = json_data.get('quantity')

    if not product_id or not product_quantity:
        return jsonify({'message': 'Product ID and quantity are required.'}), 400

    try:
        user_Input_Product_Id = int(product_id["id"])
        user_Input_Product_Quantity = int(product_quantity)
    except ValueError:
        return jsonify({'message': 'Invalid product Id or quantity.'}), 400

    productById = Product.query.filter_by(id=user_Input_Product_Id).first() 
    if not productById:
        return jsonify({'message': 'Product not found.'}), 404

    logged_in_user = User.query.filter_by(username=app.config['LOGGED_IN_USER']).first()

    user_Cart_Product = Cart.query.filter_by(user_id=logged_in_user.id, product_id=user_Input_Product_Id).first()

    if user_Cart_Product:
        user_Cart_Product.quantity +=  user_Input_Product_Quantity
        database.session.commit()
        return jsonify({'message': 'Product quantity updated in the cart.'}), 200
    else:
        cart_item = Cart(user_id=logged_in_user.id, product_id=user_Input_Product_Id, quantity= user_Input_Product_Quantity)
        database.session.add(cart_item)
        database.session.commit()
        return jsonify({'message': 'Product added to cart.'}), 201


@app.route('/add_review', methods=['POST'])
def add_review():
    if not app.config['USER_LOGGED_IN']:
        return jsonify({'message': 'You must be logged in to add a review.'}), 403

    json_data = request.get_json()
    user_Input_Product = json_data.get('product_id')
    user_Input_Product_Id = user_Input_Product.get('id')
    user_Input_Rating = int(json_data.get('rating'))
    user_Input_Comment = str(json_data.get('comment'))

    if not (1 <= user_Input_Rating <= 5):
        return jsonify({'message': 'Rating must be between 1 and 5.'}), 400

    
    productById = Product.query.filter_by(id=user_Input_Product_Id).first()

    if not productById:
        return jsonify({'message': 'Product not found.'}), 404

    logged_in_user = User.query.filter_by(username=app.config['LOGGED_IN_USER']).first()

    review = Review(product_id=user_Input_Product_Id, user_id=logged_in_user.id, rating=user_Input_Rating, comment=user_Input_Comment)
    database.session.add(review)
    database.session.commit()

    return jsonify({'message': 'Review added successfully'}), 201


@app.route('/view_cart', methods=['GET'])
def view_cart():
    if not app.config['USER_LOGGED_IN']:
        return jsonify({'message': 'You must be logged in to view your cart.'}), 403

    logged_in_user = User.query.filter_by(username=app.config['LOGGED_IN_USER']).first()
    cart_items = Cart.query.filter_by(user_id=logged_in_user.id).all()
    
    user_cart_items = []
    user_cart_total_amount = 0.0  
    
    for item in cart_items:
        product = Product.query.get(item.product_id)
        item_total = product.price * item.quantity  
    
        user_cart_items.append({
            'product_id': item.product_id,
            'product_name': product.name,
            'quantity': item.quantity,
            'price': round(product.price, 2),  
            'total_price': round(item_total, 2)  
        })
        
        user_cart_total_amount += item_total
    
    user_cart_total_amount = round(user_cart_total_amount, 2)

    return jsonify({'items': user_cart_items, 'total_amount': user_cart_total_amount}), 200


def create_tables():
    with app.app_context():
        database.create_all()

        if not User.query.first():
            hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
            admin_user = User(username="admin", password=hashed_password)
            database.session.add(admin_user)
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
