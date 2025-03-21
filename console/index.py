import requests
BASE_URL = 'http://127.0.0.1:5000' 

USER_LOGGED_IN = False
LOGGED_IN_USER = None

def print_main_menu():
    print("\n1) Login")
    print("2) Signup")
    print("3) Exit")

def print_user_menu():
    print("\n1. View Cart")
    print("2. List Categories")
    print("3. Logout")



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


def main():
    global USER_LOGGED_IN, LOGGED_IN_USER
    while True:
        if not USER_LOGGED_IN:
            print_main_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                login()
            elif choice == '2':
                signup()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")
        else:
            print_user_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                break
            elif choice == '2':
                break
            elif choice == '3':
                logout()
            else:
                print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
