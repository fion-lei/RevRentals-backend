# Add Reservation, Works for motorcycle, gear, and lot
from datetime import datetime
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory

class AddReservationView(APIView):
    def post(self, request):
        try:
            data = request.data
            profile_id = data.get("profile_id")
            product_no = data.get("product_no")
            lot_no = data.get("lot_no")
            vin = data.get("vin")
            start_date = data.get("start_date")
            end_date = data.get("end_date")

            with connection.cursor() as cursor:
                # Fetch the Admin ID (assuming there's only one admin)
                cursor.execute("SELECT admin_id FROM admin LIMIT 1")
                admin_id = cursor.fetchone()[0]

                # Validate that one of VIN, Lot_No, or Product_No is provided
                if not any([vin, lot_no, product_no]):
                    return Response({"Error": "Missing one of three parameters (VIN, Lot_No, Product_No)"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Initialize seller_id to None
                seller_id = None

                # Retrieve Seller_ID based on the input type
                if vin:
                    cursor.execute("""
                        SELECT p.Profile_ID
                        FROM motorized_vehicle mv
                        INNER JOIN garage g ON mv.Garage_ID = g.Garage_ID
                        INNER JOIN has h ON g.Garage_ID = h.Garage_ID
                        INNER JOIN profile p ON h.Profile_ID = p.Profile_ID
                        WHERE mv.VIN = %s
                    """, [vin])
                    result = cursor.fetchone()
                    if result:
                        seller_id = result[0]

                elif product_no:
                    cursor.execute("""
                        SELECT p.Profile_ID
                        FROM gear g
                        INNER JOIN garage gr ON g.Garage_ID = gr.Garage_ID
                        INNER JOIN has h ON gr.Garage_ID = h.Garage_ID
                        INNER JOIN profile p ON h.Profile_ID = p.Profile_ID
                        WHERE g.Product_No = %s
                    """, [product_no])
                    result = cursor.fetchone()
                    if result:
                        seller_id = result[0]

                elif lot_no:
                    seller_id = admin_id

                if not seller_id:
                    return Response({"Error": "Could not find the Seller_ID for the provided VIN, Product_No, or Lot_No."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Set status based on item type
                status_value = "Pending Approval"

                # Insert the reservation
                cursor.execute("""
                    INSERT INTO reservation(Profile_ID, Admin_ID, Product_no, VIN, Lot_No, Start_Date, End_Date, Status, Seller_ID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [profile_id, admin_id, product_no, vin, lot_no, start_date, end_date, status_value, seller_id])

                # Get the reservation number
                cursor.execute("""
                    SELECT Reservation_No
                    FROM reservation
                    WHERE Profile_ID = %s
                    AND Admin_ID = %s
                    AND Start_Date = %s
                    AND End_Date = %s
                    AND Status = %s
                    ORDER BY Reservation_No DESC
                    LIMIT 1
                """, [profile_id, admin_id, start_date, end_date, status_value])
                
                reservation_no = cursor.fetchone()[0]

                # If Lot_No, call AddAgreementView
                if lot_no:
                    factory = APIRequestFactory()
                    agreement_request = factory.post(
                        "/api/add-agreement/",
                        {"reservation_no": reservation_no},
                        format="json"
                    )
                    agreement_view = AddAgreementView.as_view()
                    response = agreement_view(agreement_request)

                    # Ensure the response for the reservation returns 201 Created
                    if response.status_code == 200:
                        return Response(
                            {"success": True,
                             "message": "Reservation and agreement added successfully.",
                             "reservation_no": reservation_no},
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return response

                return Response(
                    {"success": True, "message": "Reservation added successfully."},
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            print("Error occurred:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: Get agreement via reservation_no
class GetAgreementView(APIView):
    def get(self, request, reservation_no):
        try:
            with connection.cursor() as cursor:
                # Fetch agreement details based on reservation_no
                cursor.execute("""
                    SELECT Agreement_ID, Garage_ID, Rental_Overview, Damage_Compensation, Agreement_Fee
                    FROM agreement
                    WHERE Reservation_No = %s
                """, [reservation_no])
                
                agreement = cursor.fetchone()
                if not agreement:
                    return Response({"error": "No agreement found for this reservation."}, status=status.HTTP_404_NOT_FOUND)

                agreement_id, garage_id, rental_overview, damage_compensation, agreement_fee = agreement

                return Response({
                    "agreement": {
                        "Agreement_ID": agreement_id,
                        "Garage_ID": garage_id,
                        "Rental_Overview": rental_overview,
                        "Damage_Compensation": damage_compensation,
                        "Agreement_Fee": float(agreement_fee)
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: Get transaction details via reservation_no
class GetTransactionView(APIView):
    def get(self, request, reservation_no):
        try:
            with connection.cursor() as cursor:
                # Fetch transaction details based on reservation_no
                cursor.execute("""
                    SELECT t.Transaction_ID, t.Agreement_ID, t.Garage_ID, t.Pay_Date, t.Payment_Method, a.Agreement_Fee
                    FROM transaction t
                    JOIN agreement a ON t.Agreement_ID = a.Agreement_ID
                    WHERE t.Reservation_No = %s
                """, [reservation_no])
                
                transaction = cursor.fetchone()
                if not transaction:
                    return Response({"error": "No transaction found for this reservation."}, status=status.HTTP_404_NOT_FOUND)

                transaction_id, agreement_id, garage_id, pay_date, payment_method, agreement_fee = transaction

                return Response({
                    "transaction": {
                        "Transaction_ID": transaction_id,
                        "Agreement_ID": agreement_id,
                        "Garage_ID": garage_id,
                        "Pay_Date": pay_date,
                        "Payment_Method": payment_method,
                        "Amount_Paid": float(agreement_fee)
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: Add agreement
class AddAgreementView(APIView):
    def post(self, request):
        try:
            data = request.data
            reservation_no = data.get("reservation_no")

            with connection.cursor() as cursor:
                # Check if reservation exists and is not already approved
                cursor.execute(
                """
                    SELECT Status FROM reservation WHERE Reservation_No = %s
                """, [reservation_no])

                result = cursor.fetchone()
                if not result:
                    return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

                res_status = result[0]
                if res_status == 'Approved':
                    return Response({"error": "Reservation is already approved."}, status=status.HTTP_400_BAD_REQUEST)

                # Update reservation status to "Approved"
                cursor.execute("""
                    UPDATE reservation
                    SET Status = 'Approved'
                    WHERE Reservation_No = %s
                """, [reservation_no])

                # Fetch reservation details
                cursor.execute("""
                    SELECT r.Start_Date, r.End_Date, r.VIN, r.Product_No, r.Lot_No, g.Garage_ID
                    FROM reservation r
                    JOIN garage g ON g.Profile_ID = r.Profile_ID
                    WHERE r.Reservation_No = %s
                """, [reservation_no])
                reservation = cursor.fetchone()

                if not reservation:
                    return Response(
                        {"error": "Reservation not found or not approved."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                start_date, end_date, vin, product_no, lot_no, garage_id = reservation

                # Identify reservation type and fetch item details
                if vin:
                    cursor.execute("""
                        SELECT Model, Rental_Price
                        FROM motorized_vehicle
                        WHERE VIN = %s
                    """, [vin])
                    item_data = cursor.fetchone()

                    if not item_data:
                        return Response({"error": "Motorized vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

                    item_name, rental_price = item_data
                    item_type = "Motorized Vehicle"
                elif product_no:
                    cursor.execute("""
                        SELECT Gear_Name, GRentalPrice
                        FROM gear
                        WHERE Product_No = %s
                    """, [product_no])
                    item_data = cursor.fetchone()

                    if not item_data:
                        return Response({"error": "Gear not found."}, status=status.HTTP_404_NOT_FOUND)

                    item_name, rental_price = item_data
                    item_type = "Gear"
                elif lot_no:
                    cursor.execute("""
                        SELECT LAddress, LRentalPrice
                        FROM storage_lot
                        WHERE Lot_No = %s
                    """, [lot_no])
                    item_data = cursor.fetchone()

                    if not item_data:
                        return Response({"error": "Storage lot not found."}, status=status.HTTP_404_NOT_FOUND)

                    item_name, rental_price = item_data
                    item_type = "Storage Lot"
                else:
                    return Response(
                        {"error": "Invalid reservation - no item found."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Calculate rental overview and fee
                rental_days = (end_date - start_date).days + 1
                agreement_fee = rental_price * rental_days
                rental_overview = f"{item_type} rental for {rental_days} days: {start_date} to {end_date}"

                # Set a fixed damage compensation
                if lot_no:
                    damage_compensation = 0
                else:
                    damage_compensation = 200

                # Insert into agreement table
                cursor.execute("""
                    INSERT INTO agreement (Agreement_ID, Reservation_No, Garage_ID, Rental_Overview, Damage_Compensation, Agreement_Fee)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [
                    reservation_no,
                    reservation_no,
                    garage_id,
                    rental_overview,
                    damage_compensation,
                    agreement_fee
                ])

            return Response({
                "success": True,
                "message": "Reservation approved and agreement created successfully.",
                "item_name": item_name,
                "item_type": item_type,
                "rental_overview": rental_overview,
                "agreement_fee": agreement_fee,
                "damage_compensation": damage_compensation
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO: Add transaction
class AddTransactionView(APIView):
    def post(self, request):
        try:
            data = request.data
            agreement_id = data.get("agreement_id")
            payment_method = data.get("payment_method")

            if not agreement_id:
                return Response({"error": "Agreement ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                # Fetch agreement details
                cursor.execute("""
                    SELECT Agreement_Fee, Garage_ID, Reservation_No
                    FROM agreement
                    WHERE Agreement_ID = %s
                """, [agreement_id])
                
                agreement = cursor.fetchone()
                if not agreement:
                    return Response({"error": "Agreement not found."}, status=status.HTTP_404_NOT_FOUND)

                agreement_fee, garage_id, reservation_no = agreement

                # Insert transaction into the table
                cursor.execute("""
                    INSERT INTO transaction (Transaction_ID, Agreement_ID, Garage_ID, Reservation_No, Pay_Date, Payment_Method)
                    VALUES (%s, %s, %s, %s, NOW(), %s)
                """, [agreement_id, agreement_id, garage_id, reservation_no, payment_method])

                # Update reservation status to "Paid"
                cursor.execute("""
                    UPDATE reservation
                    SET Status = 'Paid'
                    WHERE Reservation_No = %s
                """, [reservation_no])

                return Response({
                    "success": True,
                    "message": "Transaction added successfully.",
                    "agreement_id": agreement_id,
                    "payment_method": payment_method,
                    "amount_paid": float(agreement_fee)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ViewReservationDetails(APIView):
    def get(self, request, reservation_no):
        try:
            with connection.cursor() as cursor:
                # First get the basic reservation and profile info
                cursor.execute("""
                    SELECT 
                        r.Reservation_No,
                        r.Start_Date,
                        r.End_Date,
                        p.First_Name,
                        p.Last_Name,
                        r.VIN,
                        r.Product_No,
                        r.Lot_No,
                        r.Status
                    FROM reservation r
                    JOIN profile p ON r.Profile_ID = p.Profile_ID
                    WHERE r.Reservation_No = %s
                """, [reservation_no])
                
                row = cursor.fetchone()
                
                if not row:
                    return Response(
                        {"error": "Reservation not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
         
                item_name = None
                item_name = None
                # Unpack the basic info
                # reservation_no, start_date, end_date, first_name, last_name, vin, product_no, lot_no = row
                reservation_no, start_date, end_date, first_name, last_name, vin, product_no, lot_no, reservation_status = row
                item_name = None
                rental_price = None

                # Check which type of reservation it is and get the specific details
                if vin:
                    cursor.execute("""
                        SELECT Model, Rental_Price 
                        FROM motorized_vehicle 
                        WHERE VIN = %s
                    """, [vin])
                    vehicle_info = cursor.fetchone()
                    if vehicle_info:
                        item_name = vehicle_info[0]
                        rental_price = float(vehicle_info[1])
                
                elif product_no:
                    cursor.execute("""
                        SELECT Gear_Name, GRentalPrice 
                        FROM gear 
                        WHERE Product_No = %s
                    """, [product_no])
                    gear_info = cursor.fetchone()
                    if gear_info:
                        item_name = gear_info[0]
                        rental_price = float(gear_info[1])
                
                elif lot_no:
                    cursor.execute("""
                        SELECT LAddress, LRentalPrice
                        FROM storage_lot 
                        WHERE Lot_No = %s
                    """, [lot_no])
                    lot_info = cursor.fetchone()
                    if lot_info:
                        item_name = lot_info[0]
                        rental_price = float(lot_info[1])
                
                # Calculate rental duration and total price
                duration = (end_date - start_date).days + 1
                total_price = rental_price * duration if rental_price else 0
                
                return Response({
                    "reservation_no": reservation_no,
                    "start_date": start_date,
                    "end_date": end_date,
                    "renter_first_name": first_name,
                    "renter_last_name": last_name,
                    "item_name": item_name,
                    "rental_price": rental_price,
                    "duration_days": duration,
                    "total_price": total_price,
                    "status":reservation_status
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

class CheckActiveLotRentalView(APIView):
    def get(self, request, profile_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        r.Reservation_No,
                        r.Lot_No,
                        sl.LAddress,
                        r.Start_Date,
                        r.End_Date
                    FROM reservation r
                    JOIN storage_lot sl ON r.Lot_No = sl.Lot_No
                    WHERE r.Profile_ID = %s
                    AND r.Status = 'Paid'
                    AND r.End_Date >= CURRENT_DATE
                    AND r.Lot_No IS NOT NULL
                """, [profile_id])
                
                rental = cursor.fetchone()
                
                if rental:
                    return Response({
                        "has_active_rental": True,
                        "rental_details": {
                            "reservation_no": rental[0],
                            "lot_no": rental[1],
                            "address": rental[2],
                            "start_date": rental[3].strftime("%Y-%m-%d"),
                            "end_date": rental[4].strftime("%Y-%m-%d")
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "has_active_rental": False
                    }, status=status.HTTP_200_OK)
                    
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )