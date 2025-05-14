def print_Main_Menu():
    print("\n1) Login")
    print("2) Signup")
    print("3) Exit")


def print_User_Menu():
    print("\n1. View Cart")
    print("2. List Categories")
    print("3. Logout")


def print_Product_Menu():
    print("\n1. Add to Cart")
    print("2. Add Review")
    print("3. Go Back")


def print_Product_Details(product):
    print("\nProduct Details:")
    print(f"Name: {product['name']}")
    print(f"Price: {product['price']}")
    print(f"Description: {product.get('description', 'No description available.')}")
    print(f"Reviews: {product.get('reviews', 'No reviews available.')}")