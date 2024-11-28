from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

#add motorized vehicle
class AddMotorizedVehicleView(APIView):
    def post(self, request):
        try:
            # Parse the incoming data
            data = request.data
            vehicle_type = data.get("vehicle_type")  # 'Motorcycle', 'Moped', or 'Dirtbike'
            vin = data.get("vin")
            registration = data.get("registration")
            rental_price = data.get("rental_price")
            color = data.get("color")
            mileage = data.get("mileage")
            insurance = data.get("insurance")
            model = data.get("model")
            specific_attribute = data.get("specific_attribute")  # Engine_Type, Cargo_Rack, or Dirt_Bike_Type
            garage_id = data.get("garage_id")

            # Validate that the garage exists
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM garage WHERE Garage_ID = %s", [garage_id])
                garage_exists = cursor.fetchone()[0]

            if not garage_exists:
                print("garage does not exist")
                return Response({"error": "Invalid garage ID."}, status=status.HTTP_400_BAD_REQUEST)

            # Insert into motorized_vehicle table
            print("inserting vehicle")
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO motorized_vehicle (VIN, Garage_ID, Registration, Rental_Price, Color, Mileage, Insurance, Model, Vehicle_Type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [vin, garage_id, registration, rental_price, color, mileage, insurance, model, vehicle_type])
            
            print("vehicle was added at:")

            # Insert into the specific child table
            if vehicle_type == "Motorcycle":
                print("motorcycle type")
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO motorcycle (VIN, Engine_Type)
                        VALUES (%s, %s)
                    """, [vin, specific_attribute])
                print("motorcycle added")

            elif vehicle_type == "Moped":
                print("Moped type")
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO moped (VIN, Cargo_Rack)
                        VALUES (%s, %s)
                    """, [vin, specific_attribute])

            elif vehicle_type == "Dirtbike":
                print("Dirtbike type")
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO dirt_bike (VIN, Terrain_Type)
                        VALUES (%s, %s)
                    """, [vin, specific_attribute])

            else:
                print("Invalid vehicle type:", vehicle_type) 
                return Response({"error": "Invalid vehicle type."}, status=status.HTTP_400_BAD_REQUEST)

            # Return success response
            print("All operations completed successfully.") 
            return Response({"success": True, "message": "Vehicle added successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle any errors and return an appropriate response
            print("Error occurred:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ViewAllMotorizedVehicles(APIView):
    def get(self, request):
        try:
            # Query the motorized_vehicle table
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT VIN, Garage_ID, Registration, Rental_Price, Color, Mileage, Insurance, Model, Vehicle_Type
                    FROM motorized_vehicle
                """)
                vehicles = cursor.fetchall()

            # Format the response data
            vehicles_data = [
                {
                    "VIN": row[0],
                    "Garage_ID": row[1],
                    "Registration": row[2],
                    "Rental_Price": float(row[3]),
                    "Color": row[4],
                    "Mileage": row[5],
                    "Insurance": row[6],
                    "Model": row[7],
                    "Vehicle_Type": row[8],
                }
                for row in vehicles
            ]

            return Response({"motorized_vehicles": vehicles_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ViewAllGarageItemsView(APIView):
    def get(self, request):
        try:
            # Get the garage_id from query parameters
            garage_id = request.query_params.get('garage_id')
            print(garage_id)
            if not garage_id:
                return Response({"error": "Garage ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Query to fetch all motorized vehicles and gear in the garage
            with connection.cursor() as cursor:
                # Fetch motorized vehicles
                cursor.execute("""
                    SELECT mv.VIN, mv.Registration, mv.Rental_Price, mv.Color, mv.Mileage, mv.Insurance, mv.Model
                    FROM motorized_vehicle AS mv
                    WHERE mv.Garage_ID = %s
                """, [garage_id])
                motorized_vehicles = cursor.fetchall()

                # Fetch gear
                cursor.execute("""
                    SELECT g.Product_No, g.Brand, g.Material, g.Type, g.Size, g.GRentalPrice, g.Gear_Name
                    FROM gear AS g
                    WHERE g.Garage_ID = %s
                """, [garage_id])
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
            return Response(
                {"motorized_vehicles": motorized_vehicles_data, "gear": gear_items_data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    #method for viewing all storage lots
class ViewAllStorageLots(APIView):
    def get(self, request):
        try:
            # Query the storage_lots table
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Lot_No, LAddress, Admin_ID
                    FROM storage_lot
                """)
                storage_lots = cursor.fetchall()

            # Format the response data
            storage_lots_data = [
                {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                }
                for row in storage_lots
            ]

            return Response({"storage_lots": storage_lots_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #method for viewing all gear items  
class ViewAllGearItems(APIView):
    def get(self, request):
        try:
            # Query the gear table
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Product_no, Garage_ID, Brand, Material, Type, Size, GRentalPrice, Gear_Name
                    FROM gear
                """)
                gear_items = cursor.fetchall()

            # Format the response data
            gear_items_data = [
                {
                    "Product_no": row[0],
                    "Garage_ID": row[1],
                    "Brand": row[2],
                    "Material": row[3],
                    "Type": row[4],
                    "Size": row[5],
                    "GRentalPrice": float(row[6]) if row[6] is not None else None,
                    "Gear_Name": row[7],
                }
                for row in gear_items
            ]

            return Response({"gear_items": gear_items_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
