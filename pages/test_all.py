#from django.test import TestCase
#from django.urls import reverse
#from rest_framework import status
#from rest_framework.test import APIClient
#from models import Account,Transaction,Ticket   
# import pytest
# from playwright.sync_api import *
# import requests

# @pytest.fixture
# def api_context(playwright: Playwright) -> APIRequestContext:
#     api_context = playwright.request.new_context(
#         base_url="http://127.0.0.1:8000",  # Update with your local API URL
#         extra_http_headers={'Content-Type': 'application/json'},
#     )
#     yield api_context
#     api_context.dispose()

# def test_registration_api(api_context: APIRequestContext):
#     # Define the registration endpoint
#     registration_endpoint = "/register"

#     # Define the data to send in the POST request
#     data = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "testpassword",
#     }

#     # Use the requests library to send a POST request with JSON data
#     response = requests.post(
#         f"{api_context.base_url}{registration_endpoint}",
#         json=data
#     )

#     # Check the response status code
#     assert response.status_code == 201

#     # Check the response JSON
#     response_json = response.json()
#     assert response_json["response"] == "Registration Successful!"
#     assert response_json["username"] == data["username"]
#     assert response_json["email"] == data["email"]
#     assert "token" in response_json
# import pytest
# from playwright.sync_api import *
# import requests

# @pytest.fixture
# def api_context(playwright: Playwright) -> APIRequestContext:
#     return playwright.request.new_context(
#         extra_http_headers={'Content-Type': 'application/json'},
#     )

# def test_registration_api(api_context: APIRequestContext):
#     # Define the registration URL
#     registration_url = "http://127.0.0.1:8000/register"  # Update with your local API URL

#     # Define the data to send in the POST request
#     data = {
#         "username": "01023912850",
#         "email": "testuser@example.com",
#         "password": "testpassword",
#     }

#     # Use the requests library to send a POST request with JSON data
#     response = requests.post(
#         registration_url,
#         json=data
#     )

#     # Check the response status code
#     assert response.status_code == 201

#     # Check the response JSON
#     response_json = response.json()
#     assert response_json["response"] == "Registration Successful!"
#     assert response_json["username"] == data["username"]
#     assert response_json["email"] == data["email"]
#     assert "token" in response_json

#     # You can also add more assertions based on your API's behavior
# @pytest.fixture
# def api_context(playwright: Playwright) -> APIRequestContext:
#     """
#     Fixture that creates and yields an APIRequestContext object using the Playwright library.

#     Args:
#         playwright (Playwright): The Playwright instance.

#     Yields:
#         APIRequestContext: The APIRequestContext object.

#     """
#     # Create a new APIRequestContext using the Playwright request.new_context() method
#     api_context = playwright.request.new_context(
#         base_url="https://dummyjson.com",
#         extra_http_headers={'Content-Type': 'application/json'},
#     )
    
#     yield api_context
    
#     # Dispose the APIRequestContext object after the test is completed
#     api_context.dispose()


# def test_createUser(api_context: APIRequestContext):
#     response = api_context.post(
#         "users/add",
#         data={
#             "firstName": "Damien",
#             "lastName": "Smith",
#             "age": 27
#         }
#     )
#     user_data = response.json()

#     assert user_data["id"] == 101
#     assert user_data["firstName"] == "Damien"

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from pages.models import Account  # Replace with the actual import path

@pytest.fixture
def authenticated_client():
    # Create a user and authenticate with a token
    user = User.objects.create_user(username='01023912858', password='testpassword')
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client

def test_deposit(authenticated_client):
    url = reverse('http://127.0.0.1:8000/TransactionView')  # Replace 'transaction-view' with your URL name
    data = {
        "transaction_type": "1",
        "amount": 100
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['message'] == 'Deposit successful'

    # Check the user's account balance
    user = User.objects.get(username='01023912858')
    account = Account.objects.get(user=user)
    assert account.account_balance == 100

def test_withdrawal(authenticated_client):
    url = reverse('transaction-view')  # Replace 'transaction-view' with your URL name
    data = {
        "transaction_type": "2",
        "amount": 50
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 201

    # Check the user's account balance
    user = User.objects.get(username='01023912858')
    account = Account.objects.get(user=user)
    assert account.account_balance == 50

def test_money_transfer(authenticated_client):
    url = reverse('transaction-view')  # Replace 'transaction-view' with your URL name
    receiver = User.objects.create_user(username='01023912859', password='receiverpassword')
    data = {
        "transaction_type": "3",
        "amount": 30,
        "receiver_username": "01023912859"
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 201

    # Check the user's account balance
    user = User.objects.get(username='01023912858')
    account = Account.objects.get(user=user)
    assert account.account_balance == 20

    # Check the receiver's account balance
    receiver_account = Account.objects.get(user=receiver)
    assert receiver_account.account_balance == 30
