from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password

# Create your views here.
class AdminLoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            username = data.get("username")
            password = data.get("password")
            print(username)
            print(password)

            # Query the database for admin username
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Admin_ID, Admin_Name, Admin_Password
                    FROM admin
                    WHERE Admin_Name = %s
                    """, [username]) 
                admin = cursor.fetchone()
                
            if admin:
                admin_id, admin_name, admin_password = admin
                if password == admin_password:
                    return Response({
                        "success": True,
                        
                        "message": "Login successful",
                        "admin_id": admin_id,
        
                    }, status = status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                    return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)     
                   
# TODO: Get admin id
class GetAdminIDView(APIView):
    def get(self, request):
        try:
            data = request.data
            print(data)
            with connection.cursor as cursor:
                cursor.execute("""
                                SELECT Admin_ID
                                FROM admin
                                """
                                )
            admin_id = cursor.fetchone()
            print(admin_id)
            return Response({"success":True, "admin_id":admin_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class ViewAllReservations(APIView):
    # View all reservations
    def get(self, request):
        try:
            # Query to fetch all reservations
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * 
                    FROM Reservation
                    """
                )
                rows = cursor.fetchall()

            # Format the data into a list of dictionaries
            reservations = [
                {
                    "Reservation_No": row[0],
                    "Profile_ID": row[1],
                    "Seller_ID": row[2],
                    "Admin_ID": row[3],
                    "Lot_No": row[4],
                    "Start_Date": row[5],
                    "End_Date": row[6],
                    "Status": row[7],
                    "VIN":row[8],
                    "Product_no": row[9]
                }
                for row in rows
            ]

            return Response({"reservations": reservations}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewAllAgreements(APIView):
    # View all agreements
    def view_all_agreements_view(self, request):
        if request.method == "GET":
            try:
                # Query to fetch all agreements
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT * 
                        FROM Agreement
                        """
                    )
                    rows = cursor.fetchall()

                # Format the data into a list of dictionaries
                agreements = [
                    {
                        "Agreement_ID": row[0],
                        "Reservation_No": row[1],
                        "Garage_ID": row[2],
                        "Rental_Overview": row[3],
                        "Damage_Compensation": row[4],
                        "Agreement_Fee": row[5]
                    }
                    for row in rows
                ]

                return Response({"agreements": agreements}, status=200)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': 'Invalid HTTP method.'}, status=405)
        
class ViewTransactions(APIView):
    def get():
        print("")
        
class AddLotListing(APIView):
    def post(self, request):
        try:
            # Parse incoming data
            data = request.data
            print(data)
            admin_id = data.get("admin_id")
            laddress = data.get("laddress")
            
            # Insert into storage lots table
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Storage_lot(Admin_ID, LAddress)
                    VALUES (%s, %s)
                               """, [admin_id, laddress])
            return Response({"success": True, "message": "Storage lot added successfully."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EditLotListing(APIView):
    def put(self, request, lot_no):
        try:
            data = request.data
            laddress = data.get("laddress")
            if not laddress or not lot_no: 
                return Response(
                    {"error": "Missing required fields: lot_no, laddress"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Use a transaction to ensure the update is atomic
            with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE Storage_Lot
                        SET Laddress = %s
                        WHERE Lot_No = %s;
                        """, [laddress, lot_no]
            )

            return Response(
                {"message": f"Lot address for lot number {lot_no} updated to {laddress}."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("Error occurred trying to update lot address:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)