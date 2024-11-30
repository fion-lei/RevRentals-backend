from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Add Motorcycle Reservation
class AddMotorcycleReservationView(APIView):
    def post(self, request):
        try:
            data = request.data
            profile_id = data.get("profile_id")
            admin_id = data.get("admin_id")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            vin = data.get("vin")
            status = "Pending Approval"
            with connection.cursor() as cursor:
                cursor.execute("""
                               INSERT INTO reservation(Profile_ID, Admin_ID, VIN, Start_Date, End_Date, Status)
                               """, [profile_id, admin_id,vin, start_date, end_date, status])
            print("reservation was added")   
            return Response({"success": True, "message": "Reservation added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle any errors and return an appropriate response
            print("Error occurred:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# TODO: Add gear reso
# Add Gear Reservation
class AddGearReservationView(APIView):
    print()


# TODO: Add lot reso  
class AddLotReservationView(APIView):
    print()
    
# TODO: Add agreement
class AddAgreementView(APIView):
    print()
    
# TODO: Add transaction
class AddTransactionView(APIView):
    print()