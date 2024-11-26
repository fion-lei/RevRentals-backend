from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# View all gear
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by material
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by type
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by size
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear by rental price
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search gear with multiple conditions
def search_gear_by_multiple_conditions_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            brand = data.get('brand')
            material = data.get('material')
            gear_type = data.get('type')
            size = data.get('size')
            max_price = data.get('grental_price')

            query = "SELECT * FROM Gear"
            conditions = []
            params = []

            if brand:
                conditions.append("brand = %s")
                params.append(brand)
            if material:
                conditions.append("material = %s")
                params.append(material)
            if gear_type:
                conditions.append("type = %s")
                params.append(gear_type)
            if size:
                conditions.append("size = %s")
                params.append(size)
            if max_price:
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
                    "GRental_Price": row[6],
                }
                for row in rows
            ]
            return JsonResponse({"gear": gear}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
