import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revRentals.settings')
django.setup()

# Import your views and necessary utilities
from myApp.views import add_profile_view, check_profile_view 
from django.test import RequestFactory

# Initialize the Django test request factory
factory = RequestFactory()

# test methods here

# Test adding a new profile
def test_add_profile():
    print("Testing add_profile_view...")
    request = factory.post(
        '/api/profile/add/',
        data=json.dumps({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "license": "AB12345",
            "username": "TESTING_1",
            "password": "password123",
            "address": "123 Elm Street",
            "overall_rating": 4.5
        }),
        content_type='application/json'
    )
    response = add_profile_view(request)
    print("Response:", response.content.decode())


# Test checking if a profile exists
def test_check_profile():
    print("\nTesting check_profile_view...")
    request = factory.get('/api/profile/check/?email=john.doe@example.com')
    response = check_profile_view(request)
    print("Response:", response.content.decode())

# Run tests
if __name__ == "__main__":
    test_add_profile()
    test_check_profile()

