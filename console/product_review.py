import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def add_Review(product_id):
    user_Input_Rating = int(input("Enter rating (1-5): "))
    user_Input_Comment = input("Enter comment (optional): ")
    response = requests.post(f'{BASE_URL}/add_review', json={'product_id': product_id, 'rating': user_Input_Rating, 'comment': user_Input_Comment})
    check_Error(response)


def check_Error(response):
    if response.status_code == 201:
        print("Review added successfully!")
    else:
        print(response.json()['message'])
    return