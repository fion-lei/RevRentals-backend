from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# Add a new profile to the database
def add_profile_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            license = data['license']
            username = data['username']
            password = data['password']
            address = data['address']
            overall_rating = data['overall_rating']

            # Insert into database
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO profile (First_Name, Last_Name, Email, License, Username, Password, Address, OverallRating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [first_name, last_name, email, license, username, password, address, overall_rating]
                )
            return JsonResponse({'message': 'Profile added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Check if a profile exists based on email
def check_profile_view(request):
    if request.method == 'GET':
        try:
            # Get email from query parameters
            email = request.GET.get('email')
            if not email:
                return JsonResponse({'error': 'Email parameter is required'}, status=400)

            # Query database for the email
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM profile WHERE Email = %s", [email])
                row = cursor.fetchone()

            if row:
                return JsonResponse({'exists': True, 'profile': row}, status=200)
            else:
                return JsonResponse({'exists': False}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Update profile details
def update_profile_view(request):
    if request.method == 'PUT':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            profile_id = data['profile_id']
            first_name = data['first_name']
            last_name = data['last_name']
            
            # Check if required fields are provided
            if not profile_id or not first_name or not last_name:
                return JsonResponse(
                    {'error': 'Profile ID, First Name, and Last Name are required.'},
                    status=400
                )

            # Insert into database
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE profile
                    SET first_name = %s, last_name = %s
                    WHERE profile_id = %s
                    """,
                    [first_name, last_name, profile_id]
                )
                
                # Check if any rows were updated
                if cursor.rowcount == 0:
                    return JsonResponse(
                        {'error': 'Profile not found or no changes made.'},
                        status=404
                    )
                    
            return JsonResponse({'message': 'Profile updated successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Update profile details
def update_address_view(request):
    if request.method == 'PUT':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            profile_id = data['profile_id']
            address = data['address']
            
            # Check if required fields are provided
            if not profile_id or not address:
                return JsonResponse(
                    {'error': 'Profile ID and address are required.'},
                    status=400
                )

            # Insert into database
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE profile
                    SET address = %s
                    WHERE profile_id = %s
                    """,
                    [address, profile_id]
                )
                
                # Check if any rows were updated
                if cursor.rowcount == 0:
                    return JsonResponse(
                        {'error': 'Profile not found or no changes made.'},
                        status=404
                    )
                    
            return JsonResponse({'message': 'Profile updated successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
