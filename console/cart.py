import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def view_Cart():
    response = requests.get(f'{BASE_URL}/view_cart')
    if response.status_code == 200:
        cart_items = response.json()
        if cart_items:
            print("\nYour Cart:")
            for item in cart_items['items']:
                print(f" ProductID:- { item['product_id']} Product Name: { item['product_name']}, Quantity: {item['quantity']}, Price: {item['price']}")
            print("\nTotal Amount: ", cart_items['total_amount'])

            remove_choice = input("Enter product ID to reduce quantity or remove (or press Enter to skip): ")
            if remove_choice:
                try:
                    product_id = int(remove_choice)
                    remove_Product_From_Cart(product_id)
                except ValueError:
                    print("Invalid product ID.")
        else:
            print("Your cart is empty.")
    else:
        print("Failed to fetch cart items.")


def add_To_Cart(product_id):
    quantity = int(input("Enter quantity: "))
    response = requests.post(f'{BASE_URL}/add_to_cart', json={'product_id': product_id, 'quantity': quantity})
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    if response.status_code == 201:
        print("Product added to cart!")
    elif response.status_code == 200:
        print("Product added to cart!")
    else:
        print("Failed to add to cart.")
        try:
            response_data = response.json() 
            print(response_data.get('message', 'No message in response'))
        except ValueError:
            print("Response is not in JSON format.")


def remove_Product_From_Cart(product_id):
    quantity_to_remove = int(input("Enter quantity to remove: "))
    
    if quantity_to_remove <= 0:
        print("Quantity to remove must be greater than 0.")
        return
    
    response = requests.put(f'{BASE_URL}/update_cart_quantity', json={'product_id': product_id, 'quantity_to_remove': quantity_to_remove})
    
    if response.status_code == 200:
        print("Product quantity updated successfully.")
    else:
        print("Failed to update product quantity in the cart.")