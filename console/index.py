import requests
BASE_URL = 'http://127.0.0.1:5000' 

USER_LOGGED_IN = False
LOGGED_IN_USER = None

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


def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = requests.post(f'{BASE_URL}/signup', json={'username': username, 'password': password})
    if response.status_code == 201:
        print("Signup successful!")
    else:
        print("Signup failed.")


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


def view_Cart():
    return


def view_Categories():
    return


def view_Products_By_Category():
    return


def view_Product_Details():
    return


def add_To_Cart():
    return 


def add_Review():
    return


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
            handle_product_details(category_choice, products)
    else:
        print("Currently No details available for this Product.")


def handle_product_details(category_choice, products):
    product_choice = int(input("Enter product ID to view details: "))
    product = view_Product_Details(product_choice, category_choice)
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
