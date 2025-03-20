from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/ecommerce'
app.config['SECRET_KEY'] = 'your_secret_key'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(120), nullable=False)

def create_tables():
    with app.app_context():
        database.create_all()

        if not User.query.first():
            hashed_password = bcrypt.generate_password_hash("admin").decode('utf-8')
            user1 = User(username="admin", password=hashed_password)
            database.session.add(user1)
            database.session.commit()


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
