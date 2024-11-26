import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revRentals.settings')
django.setup()

# Import your views and necessary utilities
from myApp.profile_views import add_profile_view, check_profile_view, update_profile_view, update_address_view
from myApp.vehicle_views import get_vehicles_view, search_by_engine_view, search_by_cargo_view, search_by_dirtbike_type_view, search_by_color_view, search_by_rental_price_view,search_by_mileage_view, search_by_multiple_conditions_view
from myApp.gear_views import get_all_gear_view, search_gear_by_brand_view, search_gear_by_material_view, search_gear_by_type_view, search_gear_by_size_view, search_gear_by_rental_price_view, search_gear_by_multiple_conditions_view
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
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "license": "AB12345",
            "username": "TESTING_2",
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
    request = factory.get('/api/profile/check/?email=jane.doe@example.com')
    response = check_profile_view(request)
    print("Response:", response.content.decode())

# Test updating a profile
def test_update_profile():
    print("\nTesting update_profile_view...")
    request = factory.put(
        '/api/profile/update/',
        data=json.dumps ({
            "profile_id": 18,
            "first_name": "update",
            "last_name": "test"
        }),
        content_type='application/json'
    )
    response = update_profile_view(request)
    print("Response:", response.content.decode())

# Test updating address
def test_update_address():
    print("\nTesting update_address_view...")
    request = factory.put(
        '/api/profile/address/',
        data=json.dumps ({
            "profile_id": 18,
            "address": "123 address update"
        }),
        content_type='application/json'
    )
    response = update_address_view(request)
    print("Response:", response.content.decode())

# Test getting all motorized vehicles
def test_get_vehicles_view():
    print("\nTesting get_vehicles_view...")
    request = factory.get(
        '/api/motorized_vehicle/get',
        content_type='application/json'
    )
    response = get_vehicles_view(request)
    print("Response:", response.content.decode())
        
def test_search_by_engine_view():
    print("\nTesting search_by_engine_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/engine',
        data = json.dumps({
            "engine_type": "Inline-4"
        }),
        content_type='application/json'
    )
    response = search_by_engine_view(request)
    print("Response:", response.content.decode())

def test_search_by_cargo_view():
    print("\nTesting search_by_cargo_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/cargo',
        data = json.dumps({
            "cargo_rack": "True"
        }),
        content_type='application/json'
    )
    response = search_by_cargo_view(request)
    print("Response:", response.content.decode())

# Test searching dirtbikes by dirt bike type
def test_search_by_dirtbike_type_view():
    print("\nTesting search_by_dirtbike_type_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/dirtbike',
        data=json.dumps({
            "dirt_bike_type": "Adventure"
        }),
        content_type='application/json'
    )
    response = search_by_dirtbike_type_view(request)
    print("Response:", response.content.decode())
# Test searching motorized vehicles by color
def test_search_by_color_view():
    print("\nTesting search_by_color_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/color',
        data=json.dumps({
            "color": "White"
        }),
        content_type='application/json'
    )
    response = search_by_color_view(request)
    print("Response:", response.content.decode())
    
# Test searching motorized vehicles by rental price
def test_search_by_rental_price_view():
    print("\nTesting search_by_rental_price_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/price',
        data=json.dumps({
            "rental_price": 200
        }),
        content_type='application/json'
    )
    response = search_by_rental_price_view(request)
    print("Response:", response.content.decode())

# Test searching motorized vehicles by mileage
def test_search_by_mileage_view():
    print("\nTesting search_by_mileage_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/mileage',
        data=json.dumps({
            "mileage": 5000
        }),
        content_type='application/json'
    )
    response = search_by_mileage_view(request)
    print("Response:", response.content.decode())

# Test searching motorized vehicles with multiple conditions
def test_search_by_multiple_conditions_view():
    print("\nTesting search_by_multiple_conditions_view...")
    request = factory.post(
        '/api/motorized_vehicle/search/multiple',
        data=json.dumps({
            "mileage": 5000,
            "rental_price": 150,
            "color": "Green",
            "engine_type": "Inline-4",
            #"cargo_rack": True,
            #"dirt_bike_type": "Adventure",
            "service_details": "Oil Change"
        }),
        content_type='application/json'
    )
    response = search_by_multiple_conditions_view(request)
    print("Response:", response.content.decode())

# Test getting all gear
def test_get_all_gear_view():
    print("\nTesting get_all_gear_view...")
    request = factory.get('/api/gear/all', content_type='application/json')
    response = get_all_gear_view(request)
    print("Response:", response.content.decode())

# Test searching gear by brand
def test_search_gear_by_brand_view():
    print("\nTesting search_gear_by_brand_view...")
    request = factory.post(
        '/api/gear/search/brand',
        data=json.dumps({"brand": "Shoei"}),
        content_type='application/json'
    )
    response = search_gear_by_brand_view(request)
    print("Response:", response.content.decode())

# Test searching gear by material
def test_search_gear_by_material_view():
    print("\nTesting search_gear_by_material_view...")
    request = factory.post(
        '/api/gear/search/material',
        data=json.dumps({"material": "Leather"}),
        content_type='application/json'
    )
    response = search_gear_by_material_view(request)
    print("Response:", response.content.decode())

# Test searching gear by type
def test_search_gear_by_type_view():
    print("\nTesting search_gear_by_type_view...")
    request = factory.post(
        '/api/gear/search/type',
        data=json.dumps({"type": "Helmet"}),
        content_type='application/json'
    )
    response = search_gear_by_type_view(request)
    print("Response:", response.content.decode())

# Test searching gear by size
def test_search_gear_by_size_view():
    print("\nTesting search_gear_by_size_view...")
    request = factory.post(
        '/api/gear/search/size',
        data=json.dumps({"size": "L"}),
        content_type='application/json'
    )
    response = search_gear_by_size_view(request)
    print("Response:", response.content.decode())

# Test searching geary by price
def test_search_gear_by_rental_price_view():
    print("\nTesting search_gear_by_rental_price_view...")
    request = factory.post(
        '/api/gear/search/price',
        data=json.dumps({"grental_price": 50}),
        content_type='application/json'
    )
    response = search_gear_by_rental_price_view(request)
    print("Response:", response.content.decode())

# Test searching gear with multiple filters
def test_search_gear_by_multiple_conditions_view():
    print("\nTesting search_gear_by_multiple_conditions_view...")
    request = factory.post(
        '/api/gear/search/multiple',
        data=json.dumps({
            "brand": "Shoei",
            "material": "Plastic",
            "type": "Helmet",
            "size": "M",
            "rental_price": 60
        }),
        content_type='application/json'
    )
    response = search_gear_by_multiple_conditions_view(request)
    print("Response:", response.content.decode())


# Run tests
if __name__ == "__main__":
    test_add_profile()
    test_check_profile()
    test_update_profile()
    test_update_address()
    test_get_vehicles_view()
    test_search_by_engine_view()
    test_search_by_cargo_view()
    test_search_by_dirtbike_type_view()
    test_search_by_color_view()
    test_search_by_rental_price_view()
    test_search_by_mileage_view()
    test_search_by_multiple_conditions_view()
    test_get_all_gear_view()
    test_search_gear_by_brand_view()
    test_search_gear_by_material_view()
    test_search_gear_by_type_view()
    test_search_gear_by_size_view()
    test_search_gear_by_rental_price_view()
    test_search_gear_by_multiple_conditions_view()