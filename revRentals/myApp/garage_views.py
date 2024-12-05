from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
            
            print("vehicle was added at: %s", [garage_id])

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
        
# TODO: Add gear
class AddGearView(APIView):
    def post(self, request):
        try:
            data = request.data
            garage_id = data.get("garage_id")
            brand = data.get("brand")
            material = data.get("material")
            type = data.get("type")
            size = data.get("size")
            rental_price = data.get("rental_price")
            gear_name = data.get("gear_name")
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO gear(Garage_ID, Brand, Material, Type, Size, GRentalPrice, Gear_Name) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                               """, [garage_id, brand, material, type, size, rental_price, gear_name])
            return Response({"success": True, "message": "Gear added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
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
        
class ViewMaintenanceRecords(APIView):
    def get(self,request, vin):
        try:
            print(vin)
            with connection.cursor() as cursor:
                cursor.execute("""
                               SELECT Date, Serviced_By, Service_Details
                               FROM maintenance_record
                               WHERE VIN = %s
                               """,[vin])
                maint_records = cursor.fetchall()
                if maint_records:
                    maint_records_data = [
                        {
                        "date": row[0],
                        "serviced_by": row[1],
                        "service_details": row[2]
                        } for row in maint_records
                    ]
                    return Response({"maintenance_records":maint_records_data}, status = status.HTTP_200_OK)
                else:
                    return Response({"error": "No maintenance records found for this vehicle."}, status=status.HTTP_404_NOT_FOUND)                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class AddMaintenanceRecordsView(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data:
                return Response(
                    {"error": "No maintenance records provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            with connection.cursor() as cursor:
                cursor.executemany("""
                    INSERT INTO maintenance_record(VIN, DATE, SERVICED_BY, SERVICE_DETAILS)
                    VALUES (%s, %s, %s, %s)
                               """
                               ,[
                    (record.get("vin"), record.get("date"), record.get("serviced_by"), record.get("service_details"))
                    for record in data
                ])
            print("Maintenance records added")
            return Response(
                        {"success": True, "message": "Maintenance records added successfully."},
                        status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # Handle any errors and return an appropriate response
            print("Error occurred trying to add maintenance records:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateRentalPriceViews(APIView):
    def post(self, request):
        try:
            data = request.data
            item_type = data.get('item_type')  # Expecting either 'vehicle' or 'gear'
            item_id = data.get('id')  # ID of the motorized vehicle or gear
            new_price = data.get('new_price')  # New rental price to update

            if not item_type or not item_id or not new_price:
                return Response(
                    {"error": "Missing required fields: item_type, id, or new_price"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            with connection.cursor() as cursor:
                # Update rental price for MotorizedVehicle
                if item_type == 'vehicle':
                    rows_updated = cursor.execute(
                        "UPDATE motorized_vehicle SET rental_price = %s WHERE vin = %s",
                        [new_price, item_id],
                    )
                    if rows_updated > 0:
                        return Response(
                            {"message": f"Rental price for vehicle {item_id} updated to {new_price}."},
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {"error": "Vehicle not found."},
                            status=status.HTTP_404_NOT_FOUND
                        )

                # Update rental price for Gear
                elif item_type == 'gear':
                    rows_updated = cursor.execute(
                        "UPDATE gear SET rental_price = %s WHERE product_no = %s",
                        [new_price, item_id],
                    )
                    if rows_updated > 0:
                        return Response(
                            {"message": f"Rental price for gear {item_id} updated to {new_price}."},
                            status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                            {"error": "Gear not found."},
                            status=status.HTTP_404_NOT_FOUND
                        )

                else:
                    return Response(
                        {"error": "Invalid item type. Must be 'vehicle' or 'gear'."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            
        except Exception as e:
            print("Error occurred trying to update rental price:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BuyerRentalHistoryView(APIView):
    def get(self, request, buyer_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        r.Reservation_No,
                        r.Start_Date,
                        r.End_Date,
                        r.Status,
                        t.Pay_Date AS Transaction_Date,
                        t.Payment_Method,
                        a.Rental_Overview,
                        a.Damage_Compensation,
                        a.Agreement_Fee,
                        COALESCE(mv.Model, g.Gear_Name, sl.LAddress) AS Item_Name,
                        mv.VIN,
                        g.Product_No,
                        sl.Lot_No AS Storage_Lot_No
                    FROM reservation r
                    LEFT JOIN agreement a ON r.Reservation_No = a.Reservation_No
                    LEFT JOIN transaction t ON a.Agreement_ID = t.Agreement_ID
                    LEFT JOIN motorized_vehicle mv ON r.VIN = mv.VIN
                    LEFT JOIN gear g ON r.Product_No = g.Product_No
                    LEFT JOIN storage_lot sl ON r.Lot_No = sl.Lot_No
                    WHERE r.Profile_ID = %s AND r.Status = 'Paid'
                    """,
                    [buyer_id]
                )

                rentals = cursor.fetchall()

            # Map the query result to a structured dictionary
            rental_history = [
                {
                    "reservation_no": rental[0],
                    "start_date": rental[1].strftime("%Y-%m-%d") if rental[1] else None,
                    "end_date": rental[2].strftime("%Y-%m-%d") if rental[2] else None,
                    "status": rental[3],
                    "transaction_date": rental[4].strftime("%Y-%m-%d") if rental[4] else None,
                    "payment_method": rental[5],
                    "rental_overview": rental[6],
                    "damage_compensation": rental[7],
                    "agreement_fee": rental[8],
                    "item_name": rental[9],
                    "vin": rental[10],
                    "product_no": rental[11],
                    "storage_lot_no": rental[12]
                }
                for rental in rentals
            ]

            return Response({"success": True, "rental_history": rental_history}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)