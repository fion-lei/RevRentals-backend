from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json

# Create your views here.

# View all reservations
def view_all_reservations_view(request):
    if request.method == "GET":
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
                    "Admin_ID": row[2],
                    "Lot_No": row[3],
                    "Start_Date": row[4],
                    "End_Date": row[5],
                    "Status": row[6]
                }
                for row in rows
            ]

            return JsonResponse({"reservations": reservations}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)

# View all agreements
def view_all_agreements_view(request):
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

            return JsonResponse({"agreements": agreements}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method.'}, status=405)
