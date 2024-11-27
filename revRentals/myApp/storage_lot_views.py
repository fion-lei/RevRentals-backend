from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# View all storage lots
def get_all_storage_lots_view(request):
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Storage_Lot")
                rows = cursor.fetchall()

            # Convert rows to list of dictionaries
            storage_lots = [
                {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                }
                for row in rows
            ]
            return JsonResponse({"storage_lots": storage_lots}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search lot by address
def search_storage_lot_by_address_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = data.get('address')

            if not address:
                return JsonResponse({'error': 'Address is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM Storage_Lot WHERE LAddress LIKE %s",
                    [f"%{address}%"]
                )
                rows = cursor.fetchall()

            storage_lots = [
                {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                }
                for row in rows
            ]
            return JsonResponse({"storage_lots": storage_lots}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Add a new storage lot
def add_storage_lot_view(request):
    if request.method == "POST":
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            laddress = data.get('laddress')
            admin_id = data.get('admin_id')

            # Validate required fields
            if not all([laddress, admin_id]):
                return JsonResponse({'error': 'Both laddress and admin_id are required.'}, status=400)

            # Insert into database
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Storage_Lot (LAddress, Admin_ID)
                    VALUES (%s, %s)
                    """,
                    [laddress, admin_id]
                )
                # Get the auto-generated Lot_No
                cursor.execute("SELECT LAST_INSERT_ID()")
                lot_no = cursor.fetchone()[0]

            return JsonResponse({'message': 'Storage lot added successfully.', 'lot_no': lot_no}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Only POST is allowed."}, status=405)