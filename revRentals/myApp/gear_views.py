from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class SearchGearByMultipleConditionsView(APIView):
    # Search gear items with multiple filtering conditions
    def get(self, request, *args, **kwargs):
        try:
            # Extract search parameters
            brand = request.GET.get('brand', "Any")
            material = request.GET.get('material', "Any")
            gear_type = request.GET.get('type', "All")
            size = request.GET.get('size', "Any")
            max_price = request.GET.get('grental_price', "Any")

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
                conditions.append("GRentalPrice <= %s")
                params.append(max_price)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # Debugging log for query and parameters
            print("Executing query with params:", params)

            # Execute query
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

            # Process results
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

            print(f"Filtered gear: {gear}")  # Debugging

            return JsonResponse({"gear": gear}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class GetAllGearView(APIView):
    # Retrieve all gear
    def get(self, request, *args, **kwargs):
        try:
            # Query to fetch all gear
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM gear")
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