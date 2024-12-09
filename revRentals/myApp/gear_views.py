from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# View all gear
@csrf_exempt
def get_all_gear_view(request):
    if request.method == "GET":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM gear")
                rows = cursor.fetchall()

            # Convert rows to list of dictionaries
            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by brand
@csrf_exempt
def search_gear_by_brand_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            brand = data.get('brand')

            if not brand:
                return JsonResponse({'error': 'Brand is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT *
                    FROM gear
                    WHERE brand = %s
                    """,
                    [brand]
                )
                rows = cursor.fetchall()

            # Convert rows to list of dictionaries
            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            ]
            print(f"Filtered gear: {gear}")
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by material
@csrf_exempt
def search_gear_by_material_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            material = data.get('material')

            if not material:
                return JsonResponse({'error': 'Material is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM gear
                    WHERE material = %s
                    """,
                    [material]
                )
                rows = cursor.fetchall()

            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            
            ]

            print(f"Filtered gear: {gear}") #debugging
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by type
@csrf_exempt
def search_gear_by_type_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            gear_type = data.get('type')

            if not gear_type:
                return JsonResponse({'error': 'Gear type is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT *
                    FROM gear
                    WHERE type = %s
                    """,
                    [gear_type]
                )
                rows = cursor.fetchall()

            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            ]

            print(f"Filtered gear: {gear}") #debugging
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by size
@csrf_exempt
def search_gear_by_size_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            size = data.get('size')

            if not size:
                return JsonResponse({'error': 'Size is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM gear
                    WHERE size = %s
                    """,
                    [size]
                )
                rows = cursor.fetchall()

            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            ]
            print(f"Filtered gear: {gear}") #debugging
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by rental price
@csrf_exempt
def search_gear_by_rental_price_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            max_price = data.get('grental_price')

            if not max_price:
                return JsonResponse({'error': 'Maximum rental price is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM gear
                    WHERE grental_price < %s
                    """,
                    [max_price]
                )
                rows = cursor.fetchall()

            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            ]
            print(f"Filtered gear: {gear}") #debugging
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear with multiple conditions
@csrf_exempt
def search_gear_by_multiple_conditions_view(request):
    if request.method == "GET":
        try:
            #data = json.loads(request.body)

            brand = request.GET.get('brand', "Any")
            material = request.GET.get('material', "Any")
            gear_type = request.GET.get('type', "All")
            size = request.GET.get('size', "Any")
            max_price = request.GET.get('grental_price', "Any")

            #For debugging
            print("Brand: ", brand, 
                  "Rental price: ", max_price,
                  "Type: ", gear_type,
                  "Size: ", size,
                  "Material: ", material,
                    )
            
            print("Request Data: ", request.GET)

            query = "SELECT * FROM Gear"
            conditions = []
            params = []

            if brand != "Any":
                conditions.append("brand = %s")
                params.append(brand)
            if material != "Any":
                conditions.append("material = %s")
                params.append(material)
            if gear_type != "All":
                conditions.append("type = %s")
                params.append(gear_type)
            if size != "Any":
                conditions.append("size = %s")
                params.append(size)
            if max_price != "Any":
                conditions.append("grental_price < %s")
                params.append(max_price)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

            gear = [
                {
                    "Product_No": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": row[6],
                    "Gear_Name": row[7],
                }
                for row in rows
            ]

            print(f"Filtered multiple: {gear}") 

            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def insert_gear_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            garage_id = data.get('garage_id')
            brand = data.get('brand')
            material = data.get('material')
            gear_type = data.get('type')
            size = data.get('size')
            rental_price = data.get('rental_price')
            gear_name = data.get('gear_name', None)  # Optional field with default None

            # Validate required fields
            if not all([garage_id, brand, material, gear_type, size, rental_price]):
                return JsonResponse({'error': 'All fields except gear_name are required.'}, status=400)

            # Check the number of gear items in the garage
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM Gear WHERE Garage_ID = %s
                    """,
                    [garage_id]
                )
                gear_count = cursor.fetchone()[0]

            if gear_count >= 5:
                return JsonResponse({'error': 'You can only have up to 5 gear items listed in your garage.'}, status=403)

            # Insert into Gear table
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Gear (Garage_ID, Brand, Material, Type, Size, GRentalPrice, Gear_Name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [garage_id, brand, material, gear_type, size, rental_price, gear_name]
                )

            return JsonResponse({'message': 'Gear added successfully.'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

def delete_gear_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            profile_id = data.get('profile_id')

            # Validate required fields
            if not profile_id:
                return JsonResponse({'error': 'Profile ID is required.'}, status=400)

            # Delete query for gear
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM Gear
                    WHERE Product_No IN (
                        SELECT GE.Product_No
                        FROM Gear AS GE
                        NATURAL JOIN Garage AS G
                        JOIN Has AS H ON H.Garage_ID = G.Garage_ID
                        WHERE H.Profile_ID = %s
                    )
                    """,
                    [profile_id]
                )

            return JsonResponse({'message': f"Gear associated with Profile ID {profile_id} deleted successfully."}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
