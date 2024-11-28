import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revRentals.settings')
django.setup()

# Import your views and necessary utilities
from myApp.profile_views import add_profile_view, check_profile_view, update_profile_view, update_address_view
from myApp.vehicle_views import get_vehicles_view, delete_motorized_vehicle_view, search_by_engine_view, search_by_cargo_view, search_by_dirtbike_type_view, search_by_color_view, search_by_rental_price_view,search_by_mileage_view, search_by_multiple_conditions_view, insert_motorized_vehicle_view, update_vehicle_price_view
from myApp.gear_views import get_all_gear_view, delete_gear_view, search_gear_by_brand_view, search_gear_by_material_view, search_gear_by_type_view, search_gear_by_size_view, search_gear_by_rental_price_view, search_gear_by_multiple_conditions_view, insert_gear_view
from myApp.storage_lot_views import get_all_storage_lots_view, edit_storage_lot_view, search_storage_lot_by_address_view, add_storage_lot_view, delete_storage_lot_view
from myApp.garage_views import view_all_garage_items_view
from myApp.admin_views import view_all_agreements_view, view_all_reservations_view
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

def test_get_all_storage_lots_view():
    print("\nTesting get_all_storage_lots_view...")
    request = factory.get('/api/storage_lot/all', content_type='application/json')
    response = get_all_storage_lots_view(request)
    print("Response:", response.content.decode())

def test_search_storage_lot_by_address_view():
    print("\nTesting search_storage_lot_by_address_view...")
    request = factory.post(
        '/api/storage_lot/search/address',
        data=json.dumps({"address": "123 Storage Lane"}),
        content_type='application/json'
    )
    response = search_storage_lot_by_address_view(request)
    print("Response:", response.content.decode())

def test_add_storage_lot_view():
    print("\nTesting add_storage_lot_view...")
    request = factory.post(
        '/api/storage_lot/add',
        data=json.dumps({
            "laddress": "789 New Calgary Ave",
            "admin_id": 1001
        }),
        content_type='application/json'
    )
    response = add_storage_lot_view(request)
    print("Response:", response.content.decode())
    
def test_insert_motorized_vehicle_view():
    print("\nTesting insert_motorized_vehicle_view...")

    # Test case for inserting a Motorcycle
    request = factory.post(
        '/api/motorized_vehicle/add',
        data=json.dumps({
            "vin": "VIN006",
            "garage_id": 1,
            "registration": "REG006",
            "rental_price": 150.00,
            "color": "Green",
            "mileage": 5000,
            "insurance": "Insurance1",
            "model": "Kawasaki Ninja ZX-4R",
            "vehicle_type": "motorcycle",
            "engine_type": "Inline-4"
        }),
        content_type='application/json'
    )
    response = insert_motorized_vehicle_view(request)
    print("Motorcycle Response:", response.content.decode())

    # Test case for inserting a Moped
    request = factory.post(
        '/api/motorized_vehicle/add',
        data=json.dumps({
            "vin": "VIN007",
            "garage_id": 2,
            "registration": "REG007",
            "rental_price": 120.00,
            "color": "Red",
            "mileage": 3000,
            "insurance": "Basic",
            "model": "Velocifero TENNIS 4000W",
            "vehicle_type": "moped",
            "cargo_rack": True
        }),
        content_type='application/json'
    )
    response = insert_motorized_vehicle_view(request)
    print("Moped Response:", response.content.decode())

    # Test case for inserting a Dirtbike
    request = factory.post(
        '/api/motorized_vehicle/add',
        data=json.dumps({
            "vin": "VIN008",
            "garage_id": 3,
            "registration": "REG008",
            "rental_price": 180.00,
            "color": "Blue",
            "mileage": 2000,
            "insurance": "Comprehensive",
            "model": "Honda CRF250R",
            "vehicle_type": "dirtbike",
            "dirt_bike_type": "Trail"
        }),
        content_type='application/json'
    )
    response = insert_motorized_vehicle_view(request)
    print("Dirtbike Response:", response.content.decode())

    # Test case with missing required fields
    request = factory.post(
        '/api/motorized_vehicle/add',
        data=json.dumps({
            "vin": "VIN009",
            "garage_id": 4,
            "registration": "REG009",
            "rental_price": 200.00,
            "color": "Yellow",
            "mileage": 1000,
            "insurance": "Premium",
            "model": "Unknown",
            "vehicle_type": "motorcycle"
            # Missing 'engine_type'
        }),
        content_type='application/json'
    )
    response = insert_motorized_vehicle_view(request)
    print("Missing Engine Type Response:", response.content.decode())

    # Test case for invalid vehicle type
    request = factory.post(
        '/api/motorized_vehicle/add',
        data=json.dumps({
            "vin": "VIN0010",
            "garage_id": 5,
            "registration": "REG010",
            "rental_price": 250.00,
            "color": "Black",
            "mileage": 1500,
            "insurance": "Insurance5",
            "model": "Unknown",
            "vehicle_type": "truck"  # Invalid type
        }),
        content_type='application/json'
    )
    response = insert_motorized_vehicle_view(request)
    print("Invalid Vehicle Type Response:", response.content.decode())

def test_insert_gear_view():
    print("\nTesting insert_gear_view...")

    # Test case with all fields
    request = factory.post(
        '/api/gear/add',
        data=json.dumps({
            "garage_id": 1,
            "brand": "Revit",
            "material": "Leather",
            "type": "Jacket",
            "size": "Medium",
            "rental_price": 150.00,
            "gear_name": "Racing Jacket"
        }),
        content_type='application/json'
    )
    response = insert_gear_view(request)
    print("Response with Gear Name:", response.content.decode())

def test_view_all_garage_items_view():
    print("\nTesting view_all_garage_items_view...")

    # Test case with a valid garage ID
    request = factory.get(
        '/api/garage/items',
        data={'garage_id': 1},
        content_type='application/json'
    )
    response = view_all_garage_items_view(request)
    print("Valid Garage Response:", response.content.decode())

def test_update_vehicle_price_view():
    print("\nTesting update_vehicle_price_view...")

    # Test case with valid data
    request = factory.post(
        '/api/motorized_vehicle/update_price',
        data=json.dumps({
            "profile_id": 1,
            "vin": "VIN001",
            "rental_price": 777.77
        }),
        content_type='application/json'
    )
    response = update_vehicle_price_view(request)
    print("Valid Update Response:", response.content.decode())

    # Test case with invalid Profile ID
    request = factory.post(
        '/api/motorized_vehicle/update_price',
        data=json.dumps({
            "profile_id": 999,  # Assuming this profile_id doesn't exist
            "vin": "VIN001",
            "rental_price": 777.77
        }),
        content_type='application/json'
    )
    response = update_vehicle_price_view(request)
    print("Invalid Profile ID Response:", response.content.decode())

def test_delete_motorized_vehicle_view():
    print("\nTesting delete_motorized_vehicle_view...")

    # Test case with valid data
    request = factory.post(
        '/api/motorized_vehicle/delete',
        data=json.dumps({
            "profile_id": 1,
            "vin": "VIN123"
        }),
        content_type='application/json'
    )
    response = delete_motorized_vehicle_view(request)
    print("Valid Delete Motorized Vehicle Response:", response.content.decode())


def test_delete_gear_view():
    print("\nTesting delete_gear_view...")

    # Test case with valid data
    request = factory.post(
        '/api/gear/delete',
        data=json.dumps({
            "profile_id": 1
        }),
        content_type='application/json'
    )
    response = delete_gear_view(request)
    print("Valid Delete Gear Response:", response.content.decode())

def test_delete_storage_lot_view():
    print("\nTesting delete_storage_lot_view...")

    # Test case with valid data
    request = factory.post(
        '/api/storage_lot/delete',
        data=json.dumps({
            "lot_no": 1
        }),
        content_type='application/json'
    )
    response = delete_storage_lot_view(request)
    print("Valid Delete Storage Lot Response:", response.content.decode())

def test_view_all_reservations_view():
    print("\nTesting view_all_reservations_view...")

    # Test case to fetch all reservations
    request = factory.get(
        '/api/reservations/view',
        content_type='application/json'
    )
    response = view_all_reservations_view(request)
    print("Reservations Response:", response.content.decode())

def test_view_all_agreements_view():
    print("\nTesting view_all_agreements_view...")

    # Test case to fetch all agreements
    request = factory.get(
        '/api/agreements/view',
        content_type='application/json'
    )
    response = view_all_agreements_view(request)
    print("Agreements Response:", response.content.decode())

def test_edit_storage_lot_view():
    print("\nTesting edit_storage_lot_view...")

    # Test case with valid data
    request = factory.post(
        '/api/storage_lot/edit',
        data=json.dumps({
            "lot_no": 123,
            "laddress": "Update Ave NW"
        }),
        content_type='application/json'
    )
    response = edit_storage_lot_view(request)
    print("Valid Edit Storage Lot Response:", response.content.decode())

    # Test case with missing lot number
    request = factory.post(
        '/api/storage_lot/edit',
        data=json.dumps({
            "laddress": "Update Ave NW"
        }),
        content_type='application/json'
    )
    response = edit_storage_lot_view(request)
    print("Missing Lot_No Response:", response.content.decode())


# Run tests
if __name__ == "__main__":
    # test_add_profile()
    # test_check_profile()
    # test_update_profile()
    # test_update_address()
    # test_get_vehicles_view()
    # test_search_by_engine_view()
    # test_search_by_cargo_view()
    # test_search_by_dirtbike_type_view()
    # test_search_by_color_view()
    # test_search_by_rental_price_view()
    # test_search_by_mileage_view()
    # test_search_by_multiple_conditions_view()
    # test_get_all_gear_view()
    # test_search_gear_by_brand_view()
    # test_search_gear_by_material_view()
    # test_search_gear_by_type_view()
    # test_search_gear_by_size_view()
    # test_search_gear_by_rental_price_view()
    # test_search_gear_by_multiple_conditions_view()
    # test_get_all_storage_lots_view()
    # test_search_storage_lot_by_address_view()
    # test_add_storage_lot_view()
    # test_insert_motorized_vehicle_view()
    test_insert_gear_view()
    test_view_all_garage_items_view()
    test_update_vehicle_price_view()
    test_delete_motorized_vehicle_view()
    test_delete_gear_view()
    test_delete_storage_lot_view()
