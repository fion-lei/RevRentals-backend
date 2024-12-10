from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# method for viewing all storage lots
class ViewAllStorageLots(APIView):
    def get(self, request):
        try:
            # Query the storage_lots table
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Lot_No, LAddress, Admin_ID, LRentalPrice
                    FROM storage_lot
                """)
                storage_lots = cursor.fetchall()

            # Format the response data
            storage_lots_data = [
                {
                    "Lot_No": row[0],
                    "LAddress": row[1],
                    "Admin_ID": row[2],
                    "LRentalPrice": float(row[3]) if row[3] is not None else 0.0,
                }
                for row in storage_lots
            ]

            return Response({"storage_lots": storage_lots_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
