from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class SearchByMultipleConditionsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Extract search parameters
            mileage = request.GET.get('mileage', "Any")
            rental_price = request.GET.get('rental_price', "Any")
            color = request.GET.get('color', "Any")
            insurance = request.GET.get('insurance', "Any")
            engine_type = request.GET.get('engine_type', "Any")
            cargo_rack = request.GET.get('cargo_rack', "Any")
            dirt_bike_type = request.GET.get('dirt_bike_type', "Any")
            vehicle_type = request.GET.get('vehicle', "All")

            # Debugging logs
            print("Mileage:", mileage,
                  "Rental price:", rental_price,
                  "Color:", color,
                  "Insurance:", insurance,
                  "Engine type:", engine_type,
                  "Cargo Rack:", cargo_rack,
                  "Dirt Bike Type:", dirt_bike_type,
                  "Vehicle Type:", vehicle_type)
            print("Request Data:", request.GET)

            # Base query
            query = """
                SELECT DISTINCT
                    MV.VIN,
                    MV.Garage_ID,
                    MV.Registration,
                    MV.Rental_Price,
                    MV.Color,
                    MV.Mileage,
                    MV.Insurance,
                    MV.Model,
                    MV.Vehicle_Type,
                    M.Engine_Type,
                    Mo.Cargo_Rack,
                    DB.Dirt_Bike_Type,
                    MR.SERVICE_DETAILS
                FROM 
                    motorized_vehicle AS MV
                LEFT JOIN 
                    motorcycle AS M ON MV.VIN = M.VIN
                LEFT JOIN 
                    moped AS Mo ON MV.VIN = Mo.VIN
                LEFT JOIN 
                    dirtbike AS DB ON MV.VIN = DB.VIN
                LEFT JOIN 
                    maintenance_record AS MR ON MV.VIN = MR.VIN
            """

            # Dynamically build WHERE clause
            conditions = []
            params = []

            if mileage != "Any":
                conditions.append("MV.Mileage <= %s")
                params.append(mileage)
            if rental_price != "Any":
                conditions.append("MV.Rental_Price <= %s")
                params.append(rental_price)
            if engine_type != "Any":
                conditions.append("M.Engine_Type = %s")
                params.append(engine_type)
            if cargo_rack != "Any":
                conditions.append("Mo.Cargo_Rack = %s")
                params.append(cargo_rack)
            if dirt_bike_type != "Any":
                conditions.append("DB.Dirt_Bike_Type = %s")
                params.append(dirt_bike_type)
            if insurance != "Any":
                conditions.append("MV.Insurance = %s")
                params.append(insurance)
            if vehicle_type != "All":
                conditions.append("MV.Vehicle_Type = %s")
                params.append(vehicle_type)
            if color == "Other":
                allowed_colors = [
                    'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Black', 'White'
                ]
                conditions.append("MV.Color NOT IN ({})".format(", ".join(["%s"] * len(allowed_colors))))
                params.extend(allowed_colors)
            elif color != "Any":
                conditions.append("MV.Color = %s")
                params.append(color)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)


            # Execute query
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

            # Process results
            vehicles = [
                {
                    "VIN": row[0],
                    "Garage_ID": row[1],
                    "Registration": row[2],
                    "Rental_Price": row[3],
                    "Color": row[4],
                    "Mileage": row[5],
                    "Insurance": row[6],
                    "Model": row[7],
                    "Vehicle Type": row[8],
                    "Engine_Type": row[9],
                    "Cargo_Rack": row[10] if len(row) > 10 else None,
                    "Dirt_Bike_Type": row[11] if len(row) > 11 else None,
                }
                for row in rows
            ]

            #print(f"Filtered vehicles: {vehicles}")  # Debugging

            return JsonResponse({"vehicles": vehicles}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        
class GetVIN(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT VIN
                    FROM motorized_vehicle
                    WHERE model = %s AND rental_price = %s
                    """)
                vin = cursor.fetchone()
                
            return Response({"vin": vin} , status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  

