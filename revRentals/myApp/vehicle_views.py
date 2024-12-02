from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


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
                    "Vehicle_Type": row[8]
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
            motorcycles = [
                 {
                     "VIN": row[0],
                     "Garage_ID": row[1],
                     "Registration": row[2],
                     "Rental_Price": row[3],
                     "Color": row[4],
                     "Mileage": row[5],
                     "Insurance": row[6],
                     "Model": row[7],
                     "Engine_Type": row[8]
                 }
                 for row in rows
             ]
            return JsonResponse({"motorcycles": motorcycles}, status=201)
            
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
@csrf_exempt
def search_by_color_view(request):
    if request.method == "POST":
        print("Received POST request")
        try:
            data = json.loads(request.body)
            color = data.get('color')

           # if not color:
           #     return JsonResponse({'error': 'Color is required.'}, status=400)
            if color:

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
            else:
                 with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM motorized_vehicle")
                    rows = cursor.fetchall()

            # if you want to see all details
            vehicles = [
                 {
                     "VIN": row[0],
                     "Garage_ID": row[1],
                     "Registration": row[2],
                     "Rental_Price": row[3],
                     "Color": row[4],
                     "Mileage": row[5],
                     "Insurance": row[6],
                     "Model": row[7]
                 }
                 for row in rows
             ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            #vins = [row[0] for row in rows]

            print(f"Filtered vehicles: {vehicles}") #debugging
            
            return JsonResponse({"vehicles": vehicles}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for insurance type
@csrf_exempt
def search_by_insurance_view(request):
    if request.method == "POST":
        print("Received POST request")
        try:
            data = json.loads(request.body)
            insurance = data.get('insurance')

           # if not color:
           #     return JsonResponse({'error': 'Color is required.'}, status=400)
            if insurance:

                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM motorized_vehicle
                        WHERE insurance = %s
                        """,
                        [insurance]
                    )
                    rows = cursor.fetchall()
            else:
                 with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM motorized_vehicle")
                    rows = cursor.fetchall()

            # if you want to see all details
            vehicles = [
                 {
                     "VIN": row[0],
                     "Garage_ID": row[1],
                     "Registration": row[2],
                     "Rental_Price": row[3],
                     "Color": row[4],
                     "Mileage": row[5],
                     "Insurance": row[6],
                     "Model": row[7]
                 }
                 for row in rows
             ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            #vins = [row[0] for row in rows]

            print(f"Filtered vehicles: {vehicles}") #debugging
            
            return JsonResponse({"vehicles": vehicles}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Search for motorized vehicles by rental price
@csrf_exempt
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
            vehicles = [
                 {
                     "VIN": row[0],
                     "Garage_ID": row[1],
                     "Registration": row[2],
                     "Rental_Price": row[3],
                     "Color": row[4],
                     "Mileage": row[5],
                     "Insurance": row[6],
                     "Model": row[7]
                 }
                 for row in rows
             ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            #vins = [row[0] for row in rows]

            print(f"Filtered vehicles: {vehicles}") #debugging
            
            return JsonResponse({"vehicles": vehicles}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Search for motorized vehicles by mileage
@csrf_exempt
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
            vehicles = [
                 {
                     "VIN": row[0],
                     "Garage_ID": row[1],
                     "Registration": row[2],
                     "Rental_Price": row[3],
                     "Color": row[4],
                     "Mileage": row[5],
                     "Insurance": row[6],
                     "Model": row[7]
                 }
                 for row in rows
             ]
            # return JsonResponse({"vehicles": vehicles}, status=201)
            
            # Extract VINs from rows
            #vins = [row[0] for row in rows]

            print(f"Filtered vehicles: {vehicles}") #debugging
            
            return JsonResponse({"vehicles": vehicles}, status=200)
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

def insert_motorized_vehicle_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            vin = data.get('vin')
            garage_id = data.get('garage_id')
            registration = data.get('registration')
            rental_price = data.get('rental_price')
            color = data.get('color')
            mileage = data.get('mileage')
            insurance = data.get('insurance')
            model = data.get('model')
            vehicle_type = data.get('vehicle_type')

            # Validate required fields
            if not all([vin, garage_id, registration, rental_price, color, mileage, insurance, model, vehicle_type]):
                return JsonResponse({'error': 'All fields, including vehicle_type, are required.'}, status=400)

            # Insert into Motorized_Vehicle table
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Motorized_Vehicle (VIN, Garage_ID, Registration, Rental_Price, Color, Mileage, Insurance, Model, Vehicle_Type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [vin, garage_id, registration, rental_price, color, mileage, insurance, model, vehicle_type]
                )

                # Insert into the corresponding child table
                if vehicle_type.lower() == 'motorcycle':
                    engine_type = data.get('engine_type', None)
                    cursor.execute(
                        """
                        INSERT INTO Motorcycle (VIN, Engine_Type)
                        VALUES (%s, %s)
                        """,
                        [vin, engine_type]
                    )
                elif vehicle_type.lower() == 'moped':
                    cargo_rack = data.get('cargo_rack', None)
                    cursor.execute(
                        """
                        INSERT INTO Moped (VIN, Cargo_Rack)
                        VALUES (%s, %s)
                        """,
                        [vin, cargo_rack]
                    )
                elif vehicle_type.lower() == 'dirtbike':
                    dirt_bike_type = data.get('dirt_bike_type', None)
                    cursor.execute(
                        """
                        INSERT INTO Dirtbike (VIN, Dirt_Bike_Type)
                        VALUES (%s, %s)
                        """,
                        [vin, dirt_bike_type]
                    )
                else:
                    return JsonResponse({'error': f"Invalid vehicle type: {vehicle_type}"}, status=400)

            return JsonResponse({'message': f"{vehicle_type.capitalize()} added successfully."}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

# Update motorized vehicle price
def update_vehicle_price_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            vin = data.get('vin')
            new_rental_price = data.get('rental_price')

            # Validate required fields
            if not all([profile_id, vin, new_rental_price]):
                return JsonResponse({'error': 'Profile ID, VIN, and Rental Price are required.'}, status=400)

            # Update query for motorized vehicle price
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE Motorized_Vehicle AS M
                    JOIN Garage AS G ON M.Garage_ID = G.Garage_ID
                    JOIN Has AS H ON H.Garage_ID = G.Garage_ID
                    SET M.Rental_Price = %s
                    WHERE H.Profile_ID = %s AND M.VIN = %s
                    """,
                    [new_rental_price, profile_id, vin]
                )

            return JsonResponse({'message': f"Vehicle with VIN {vin} price updated successfully to {new_rental_price}."}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

def delete_motorized_vehicle_view(request):
    if request.method == "POST":
        try:
            # Parse user input
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            vin = data.get('vin')

            # Validate required fields
            if not all([profile_id, vin]):
                return JsonResponse({'error': 'Profile ID and VIN are required.'}, status=400)

            # Delete query for motorized vehicle
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE M
                    FROM Motorized_Vehicle AS M
                    JOIN Garage AS G ON M.Garage_ID = G.Garage_ID
                    JOIN Has AS H ON H.Garage_ID = G.Garage_ID
                    WHERE H.Profile_ID = %s AND M.VIN = %s
                    """,
                    [profile_id, vin]
                )

            return JsonResponse({'message': f"Motorized vehicle with VIN {vin} deleted successfully."}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

class SearchByColorView(APIView):
    # Search for motorized vehicles by color
    def post(self, request, *args, **kwargs):
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

            vins = [row[0] for row in rows]

            return JsonResponse({"vins": vins}, status=200)

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
    
