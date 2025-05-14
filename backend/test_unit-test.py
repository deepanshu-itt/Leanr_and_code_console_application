import unittest
from index import app, database, User, Product, Category, Cart, create_tables
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class EcommerceTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.client = app.test_client()

        with app.app_context():
            database.drop_all()
            database.create_all()

            user = User(username="testuser", password=bcrypt.generate_password_hash("password").decode('utf-8'))
            category = Category(name="Electronics")
            database.session.add_all([user, category])
            database.session.commit()

            product = Product(name="Test Product", price=100, description="Sample product", category_id=category.id)
            database.session.add(product)
            database.session.commit()


    def login(self):
        return self.client.post('/login', json={'username': 'testuser', 'password': 'password'})

    def logout(self):
        return self.client.post('/logout')

    def test_signup(self):
        response = self.client.post('/signup', json={'username': 'newuser', 'password': 'newpass'})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)
    
    def test_wrong_user_login(self):
        response = self.client.post('/login', json={'username': 'newusers', 'password': 'newpasss'})
        self.assertEqual(response.status_code, 401)

    def test_login_logout(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
    
    def test_logout(self):
        self.login()
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully', response.data)

    def test_get_categories_user_authorized(self):
        self.login()
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Electronics', response.data)
    
    def test_get_categories_user_unauthorized(self):
        self.login()
        self.logout()
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 403)


    def test_get_products_by_category_authorized(self):
        self.login()
        with app.app_context():
            category = Category.query.first()
        response = self.client.get(f'/products/{category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)


    def test_get_products_by_category_unauthorized(self):
        self.login()
        self.logout()
        with app.app_context():
            category = Category.query.first()
        response = self.client.get(f'/products/{category.id}')
        self.assertEqual(response.status_code, 403)


    def test_add_to_cart_product_added(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 2})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product added to cart', response.data)


    def test_add_to_cart_without_quantity(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': product.id}})
        self.assertEqual(response.status_code, 400)


    def test_add_to_cart_invalid_input(self):
        self.login()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': 'a'}, 'quantity': 2})
        self.assertEqual(response.status_code, 400)


    def test_add_to_cart_product_not_found(self):
        self.login()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': 1011}, 'quantity': 2})
        self.assertEqual(response.status_code, 404)


    def test_update_to_cart(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
            response = self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 2})
            logged_In_User = User.query.filter_by(username='testuser').first()
            user_Cart_Product = Cart.query.filter_by(user_id=logged_In_User.id, product_id=product.id).first()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 2})
        self.assertEqual(response.status_code, 200)


    def test_add_to_cart_unauthorized(self):
        self.login()
        self.logout()
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 2})
        self.assertEqual(response.status_code, 403)

        
    def test_view_cart(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 1})
        response = self.client.get('/view_cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.data)
        
        self.logout()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 1})
        response = self.client.get('/view_cart')
        self.assertEqual(response.status_code, 403)


    def test_add_review(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/add_review', json={
            'product_id': {'id': product.id},
            'rating': 5,
            'comment': 'Excellent!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Review added successfully', response.data)
        
        response = self.client.post('/add_review', json={
            'product_id': {'id': product.id},
            'rating': 6,
            'comment': 'Excellent!'
        })
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post('/add_review', json={
            'product_id': {'id': 21},
            'rating': 2,
            'comment': 'Excellent!'
        })
        self.assertEqual(response.status_code, 404)
        
        self.logout()
        with app.app_context():
            product = Product.query.first()
        response = self.client.post('/add_review', json={
            'product_id': {'id': product.id},
            'rating': 5,
            'comment': 'Excellent!'
        })
        self.assertEqual(response.status_code, 403)


    def test_update_cart_quantity_authorized(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': product.id, 'quantity_to_remove': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product quantity removed', response.data)


    def test_update_cart_quantity_not_found(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': product.id})
        self.assertEqual(response.status_code, 400)
    
    
    def test_update_cart_product_id_not_found(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': 21, 'quantity_to_remove': 1})
        self.assertEqual(response.status_code, 404)
    

    def test_update_cart_greater_quantity(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': product.id, 'quantity_to_remove': 11})
        self.assertEqual(response.status_code, 404)


    def test_update_cart_remove_item_equal_cart(self):
        self.login()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': product.id, 'quantity_to_remove': 3})
        self.assertIn(b'Product quantity removed', response.data)
        self.assertEqual(response.status_code, 200)
        

    def test_update_cart_product_unauthorized(self):
        self.login()
        self.logout()
        with app.app_context():
            product = Product.query.first()
        self.client.post('/add_to_cart', json={'product_id': {'id': product.id}, 'quantity': 3})
        response = self.client.put('/update_cart_quantity', json={'product_id': product.id, 'quantity_to_remove': 1})
        self.assertEqual(response.status_code, 403)



if __name__ == '__main__':
    unittest.main()
