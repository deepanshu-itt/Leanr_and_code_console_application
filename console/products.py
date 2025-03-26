import requests
import os
from dotenv import load_dotenv
from menu import print_Product_Menu, print_Product_Details
from cart import add_To_Cart
from product_review import add_Review
load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def view_Products_By_Category(category_id):
    response = requests.get(f'{BASE_URL}/products/{category_id}')
    products = []
    if response.status_code == 200:
        products_In_Json = response.json()
        print("\nProducts in this category:")
        for product in  products_In_Json:
            print(f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}")
        products = products_In_Json
    else:
        print("Failed to fetch products.")

    return products  


def view_Product_Details(category_id, product_id):
    products = get_Product_List(category_id)
    
    if products:
        product = find_Product_By_Id(products, product_id)
        
        if product:
            print_Product_Details(product)
            
            loop_active = True
            while loop_active:
                print_Product_Menu()
                choice = input("Enter your choice: ")
                loop_active = not handle_User_Choice(choice, product)
        else:
            print("Product not found.")


def get_Product_List(category_id):
    response = requests.get(f'{BASE_URL}/products/{category_id}')
    json_data = None
    if response.status_code == 200:
        json_data = response.json()
    else:
        print("Failed to fetch product list.")
    return json_data


def find_Product_By_Id(products, product_id):
    return next((p for p in products if p['id'] == product_id), None)


def handle_User_Choice(choice, product):
    response = False
    if choice == '1':
        add_To_Cart(product)
    elif choice == '2':
        add_Review(product)
    elif choice == '3':
        response = True 
    else:
        print("Invalid choice. Please try again.")
    return response