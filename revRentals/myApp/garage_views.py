from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# View all garage items

def view_all_garage_items_view(request):
    if request.method == "GET":
        try:
            # Parse the query parameter to get the garage ID
            garage_id = request.GET.get('garage_id')
            if not garage_id:
                return JsonResponse({'error': 'Garage ID is required.'}, status=400)

            # Query to fetch all items (motorized vehicles and gear) in the garage
            with connection.cursor() as cursor:
                # Fetch motorized vehicles
                cursor.execute(
                    """
                    SELECT mv.VIN, mv.Registration, mv.Rental_Price, mv.Color, mv.Mileage, mv.Insurance, mv.Model
                    FROM motorized_vehicle AS mv
                    WHERE mv.Garage_ID = %s
                    """,
                    [garage_id]
                )
                motorized_vehicles = cursor.fetchall()

                # Fetch gear
                cursor.execute(
                    """
                    SELECT g.Product_No, g.Brand, g.Material, g.Type, g.Size, g.GRentalPrice, g.Gear_Name
                    FROM gear AS g
                    WHERE g.Garage_ID = %s
                    """,
                    [garage_id]
                )
                gear_items = cursor.fetchall()

            # Format the response data
            motorized_vehicles_data = [
                {
                    "VIN": row[0],
                    "Registration": row[1],
                    "Rental_Price": row[2],
                    "Color": row[3],
                    "Mileage": row[4],
                    "Insurance": row[5],
                    "Model": row[6],
                }
                for row in motorized_vehicles
            ]

            gear_items_data = [
                {
                    "Product_No": row[0],
                    "Brand": row[1],
                    "Material": row[2],
                    "Type": row[3],
                    "Size": row[4],
                    "Rental_Price": row[5],
                    "Gear_Name": row[6],
                }
                for row in gear_items
            ]

            # Combine both lists in the response
            return JsonResponse(
                {"motorized_vehicles": motorized_vehicles_data, "gear": gear_items_data},
                status=200
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
