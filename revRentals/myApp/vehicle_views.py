from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# Get all motorized vehicles
def get_vehicles_view(request):
    if request.method == "GET":
        try:
            # Query to fetch all vehicles
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM motorized_vehicle"
                )
                rows = cursor.fetchall()
                
            # Convert rows to a list of dictionaries
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
                }
                for row in rows
            ]
            return JsonResponse({"vehicles": vehicles}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorcycles by engine type
def search_by_engine_view(request):
    if request.method == "POST":
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            engine_type = data.get('engine_type')

            # Validate input
            if not engine_type:
                return JsonResponse({'error': 'Engine type is required.'}, status=400)

            # Query to fetch motorcycle by engine type
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle NATURAL JOIN motorcycle
                    WHERE engine_type = %s
                    """,
                    [engine_type]
                )
                rows = cursor.fetchall()

            # if you want to see all details
            # # Convert rows to a list of dictionaries
            # motorcycles = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7],
            #         "Engine_Type": row[8]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"motorcycles": motorcycles}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for mopeds by cargo rack
def search_by_cargo_view(request):
    if request.method == "POST":
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            cargo_rack = data.get('cargo_rack')

            # Validate input
            if not cargo_rack:
                return JsonResponse({'error': 'Cargo selection is required.'}, status=400)

            # Query to fetch motorcycle by engine type
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle NATURAL JOIN moped
                    WHERE cargo_rack = %s
                    """,
                    [cargo_rack]
                )
                rows = cursor.fetchall()
                
            # if you want to see all details
            # # Convert rows to a list of dictionaries
            # mopeds = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7],
            #         "Cargo_Rack": row[8]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"mopeds": mopeds}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for dirtbikes by dirt bike type
def search_by_dirtbike_type_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            dirt_bike_type = data.get('dirt_bike_type')

            if not dirt_bike_type:
                return JsonResponse({'error': 'Dirt Bike Type is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle NATURAL JOIN dirtbike
                    WHERE dirt_bike_type = %s
                    """,
                    [dirt_bike_type]
                )
                rows = cursor.fetchall()

            # if you want to see all details
            # dirtbikes = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7],
            #         "Dirt_Bike_Type": row[8]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"dirtbikes": dirtbikes}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorized vehicles by color
def search_by_color_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            color = data.get('color')

            if not color:
                return JsonResponse({'error': 'Color is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle
                    WHERE color = %s
                    """,
                    [color]
                )
                rows = cursor.fetchall()

            # if you want to see all details
            # vehicles = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorized vehicles by rental price
def search_by_rental_price_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            max_price = data.get('rental_price')

            if not max_price:
                return JsonResponse({'error': 'Maximum rental price is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle
                    WHERE rental_price < %s
                    """,
                    [max_price]
                )
                rows = cursor.fetchall()

            # if you want to see all details
            # vehicles = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorized vehicles by mileage
def search_by_mileage_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            max_mileage = data.get('mileage')

            if not max_mileage:
                return JsonResponse({'error': 'Maximum mileage is required.'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM motorized_vehicle
                    WHERE mileage < %s
                    """,
                    [max_mileage]
                )
                rows = cursor.fetchall()

            # if you want to see all details
            # vehicles = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7]
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorized vehicles by multiple conditions
def search_by_multiple_conditions_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Extract search parameters
            mileage = data.get('mileage')
            rental_price = data.get('rental_price')
            color = data.get('color')
            engine_type = data.get('engine_type')
            cargo_rack = data.get('cargo_rack')
            dirt_bike_type = data.get('dirt_bike_type')
            service_details = data.get('service_details')
            
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

            if mileage is not None:
                conditions.append("MV.Mileage <= %s")
                params.append(mileage)
            if rental_price is not None:
                conditions.append("MV.Rental_Price <= %s")
                params.append(rental_price)
            if color:
                conditions.append("MV.Color = %s")
                params.append(color)
            if engine_type:
                conditions.append("M.Engine_Type = %s")
                params.append(engine_type)
            if cargo_rack is not None:  # Boolean for mopeds
                conditions.append("Mo.Cargo_Rack = %s")
                params.append(cargo_rack)
            if dirt_bike_type:
                conditions.append("DB.Dirt_Bike_Type = %s")
                params.append(dirt_bike_type)
            if service_details:
                conditions.append("MR.SERVICE_DETAILS LIKE %s")
                params.append(f"%{service_details}%")

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # Execute query
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()

            # # Process results, if you want to see all details
            # vehicles = [
            #     {
            #         "VIN": row[0],
            #         "Garage_ID": row[1],
            #         "Registration": row[2],
            #         "Rental_Price": row[3],
            #         "Color": row[4],
            #         "Mileage": row[5],
            #         "Insurance": row[6],
            #         "Model": row[7],
            #         "Engine_Type": row[8],
            #         "Cargo_Rack": row[9] if len(row) > 9 else None,
            #         "Dirt_Bike_Type": row[10] if len(row) > 10 else None,
            #         "Service_Details": row[11] if len(row) > 11 else None,
            #     }
            #     for row in rows
            # ]
            # return JsonResponse({"vehicles": vehicles}, status=200)
            # Extract VINs from rows
            
            vins = [row[0] for row in rows]
            
            return JsonResponse({"vins": vins}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method. Only POST is allowed."}, status=405)
