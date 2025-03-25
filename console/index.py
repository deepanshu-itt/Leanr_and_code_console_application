import requests
from dotenv import load_dotenv
import os
from menu import print_Main_Menu, print_Product_Menu, print_User_Menu
from products import view_Product_Details, view_Products_By_Category
from cart import view_Cart, add_To_Cart
from auth import signup
from product_review import add_Review
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

USER_LOGGED_IN = False
LOGGED_IN_USER = None


def login():
    global USER_LOGGED_IN, LOGGED_IN_USER
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        USER_LOGGED_IN = True
        LOGGED_IN_USER = username
        print("Login successful!")
    else:
        print("Invalid credentials, please try again.")


def logout():
    global USER_LOGGED_IN, LOGGED_IN_USER
    response = requests.post(f'{BASE_URL}/logout')
    if response.status_code == 200:
        USER_LOGGED_IN = False
        LOGGED_IN_USER = None
        print("Logged out successfully.")
    else:
        print("Failed to log out.")


def view_Categories():
    response = requests.get(f'{BASE_URL}/categories')
    categories = []
    if response.status_code == 200:
        categories_In_Json = response.json()
        print("\nCategories:")
        for category in categories_In_Json:
            print(f"{category['id']}. {category['name']}")
        categories = categories_In_Json
    else:
        print("Failed to fetch categories.")
    return categories


def handle_User_Not_Logged_In():
    print_Main_Menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        login()
    elif choice == '2':
        signup()
    elif choice == '3':
        print("Exiting...")
        return False
    else:
        print("Invalid choice. Try again.")
    return True


def handle_User_Logged_In():
    print_User_Menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        view_Cart()
    elif choice == '2':
        handle_Categories()
    elif choice == '3':
        logout()
    else:
        print("Invalid choice. Try again.")


def handle_Categories():
    categories = view_Categories()
    if categories:
        category_choice = int(input("Enter category ID to view products: "))
        products = view_Products_By_Category(category_choice)
        is_Product_Exists(category_choice, products)
    else:
        print("No Categories currently. Internal Error.")


def is_Product_Exists(category_choice, products):
    if products:
            handle_product_details(category_choice)
    else:
        print("Currently No details available for this Product.")


def handle_product_details(category_choice):
    product_choice = int(input("Enter product ID to view details: "))
    product = view_Product_Details(category_choice, product_choice,)
    user_Want_Menu = True
    if product:
        while user_Want_Menu:
            print_Product_Menu()
            product_Menu_Action = input("Enter your choice: ")
            user_Want_Menu = handle_Product_Menu_Action(product_Menu_Action, product_choice)

    else:
        print("No Product Details available.")


def handle_Product_Menu_Action(product_Menu_Action, product_choice):
    user_Want_Menu = True
    if product_Menu_Action == '1':
        add_To_Cart(product_choice)
    elif product_Menu_Action == '2':
        add_Review(product_choice)
    elif product_Menu_Action == '3':
        user_Want_Menu = False  
    else:
        print("Invalid choice. Try again.")
    
    return user_Want_Menu
            


def main():
    global USER_LOGGED_IN, LOGGED_IN_USER
    while True:
        if not USER_LOGGED_IN:
            if not handle_User_Not_Logged_In():
                break
        else:
            handle_User_Logged_In()


if __name__ == '__main__':
    main()
