import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    response = requests.post(f'{BASE_URL}/signup', json={'username': username, 'password': password})
    if response.status_code == 201:
        print("Signup successful!")
    else:
        print("Signup failed.")