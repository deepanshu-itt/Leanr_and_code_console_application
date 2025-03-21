def print_main_menu():
    print("\n1) Login")
    print("2) Signup")
    print("3) Exit")


def signup():
    return


def login():
    return 


def print_user_menu():
    return


def logout():
    return


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
