import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')


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


def view_Cart():
    cart_items = get_Cart_Items()

    if cart_items:
        display_Cart(cart_items)
        remove_choice = get_Remove_Choice()

        if remove_choice:
            try:
                product_id = int(remove_choice)
                remove_Product_From_Cart(product_id)
            except ValueError:
                print("Invalid product ID.")


def get_Cart_Items():
    response = requests.get(f'{BASE_URL}/view_cart')
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch cart items.")
        return None


def display_Cart(cart_items):
    if cart_items:
        print("\nYour Cart:")
        for item in cart_items['items']:
            print(f" ProductID:- {item['product_id']} Product Name: {item['product_name']}, Quantity: {item['quantity']}, Price: {item['price']}")
        print("\nTotal Amount: ", cart_items['total_amount'])
    else:
        print("Your cart is empty.")

def get_Remove_Choice():
    remove_choice = input("Enter product ID to reduce quantity or remove (or press Enter to skip): ")
    return remove_choice
