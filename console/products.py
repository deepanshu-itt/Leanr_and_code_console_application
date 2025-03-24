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
    response = requests.get(f'{BASE_URL}/products/{category_id}')

    if response.status_code == 200:
        products = response.json() 
        
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            print_Product_Details(product)
            
            while True:
                
                print_Product_Menu()
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    add_To_Cart(product)
                elif choice == '2':
                    add_Review(product)
                elif choice == '3':
                    return 
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Product not found.")
    else:
        print("Failed to fetch product details.")