from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# method for viewing all storage lots
class ViewAllStorageLots(APIView):
    def get(self, request):
        try:
            # Query the storage_lots table
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Lot_No, LAddress, Admin_ID, LRentalPrice
                    FROM storage_lot
                """)
                storage_lots = cursor.fetchall()

            # Format the response data
            storage_lots_data = [
                {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                    "LRentalPrice": float(row[3]) if row[3] is not None else 0.0,
                }
                for row in storage_lots
            ]

            return Response({"storage_lots": storage_lots_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# View all storage lots
def get_all_storage_lots_view(request):
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Lot_No, LAddress, Admin_ID, LRentalPrice FROM Storage_Lot")
                rows = cursor.fetchall()
                
                # Debug print raw rows
                print("Raw rows from database:", rows)

            # Convert rows to list of dictionaries with debug prints
            storage_lots = []
            for row in rows:
                print("Processing row:", row)  # Debug print each row
                lot_dict = {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                    "LRentalPrice": float(row[3]) if row[3] is not None else 0.0,
                }
                print("Created dictionary:", lot_dict)  # Debug print created dictionary
                storage_lots.append(lot_dict)

            print("Final storage_lots list:", storage_lots)  # Debug final list
            return JsonResponse({"storage_lots": storage_lots}, status=200)
        except Exception as e:
            print("Error in get_all_storage_lots_view:", str(e))  # Debug print any errors
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

def delete_storage_lot_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            lot_no = data.get('lot_no')

            # Validate required fields
            if not lot_no:
                return JsonResponse({'error': 'Lot number is required.'}, status=400)

            # Delete query for storage lot
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM Storage_Lot
                    WHERE Lot_No = %s
                    """,
                    [lot_no]
                )

            return JsonResponse({'message': f"Storage lot with Lot_No {lot_no} deleted successfully."}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

def edit_storage_lot_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            lot_no = data.get('lot_no')
            new_address = data.get('laddress')

            # Validate required fields
            if not all([lot_no, new_address]):
                return JsonResponse({'error': 'Lot number and new address are required.'}, status=400)

            # Update query for storage lot
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE Storage_Lot
                    SET LAddress = %s
                    WHERE Lot_No = %s
                    """,
                    [new_address, lot_no]
                )

            return JsonResponse({'message': f"Storage lot with Lot_No {lot_no} updated successfully to address {new_address}."}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
