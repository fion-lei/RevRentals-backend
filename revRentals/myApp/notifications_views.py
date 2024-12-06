from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class SellerNotificationsView(APIView):
    def get(self, request, seller_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        r.Reservation_No, 
                        r.Start_Date, 
                        r.End_Date, 
                        r.Status, 
                        p.First_Name AS renter_first_name, 
                        p.Last_Name AS renter_last_name,
                        COALESCE(
                            mv.Model, 
                            g.Gear_Name, 
                            s.LAddress
                        ) AS item_name
                    FROM reservation r
                    JOIN profile p ON r.Profile_ID = p.Profile_ID
                    LEFT JOIN motorized_vehicle mv ON r.VIN = mv.VIN
                    LEFT JOIN gear g ON r.Product_No = g.Product_No
                    LEFT JOIN storage_lot s ON r.Lot_No = s.Lot_No
                    WHERE r.Seller_ID = %s AND r.Status = 'Pending Approval';
                """, [seller_id])
                reservations = cursor.fetchall()

            # Map tuples to dictionaries with proper keys
            notifications = [
                {
                    "reservation_no": res[0],
                    "item_name": res[6],  # Item name from query
                    "start_date": res[1].strftime("%Y-%m-%d") if res[1] else None,
                    "end_date": res[2].strftime("%Y-%m-%d") if res[2] else None,
                    "status": res[3],
                    "renter_first_name": res[4],
                    "renter_last_name": res[5],
                }
                for res in reservations
            ]
            print(notifications)
            return Response({"success": True, "notifications": notifications}, status=200)
        except Exception as e:
            print(f"Error in SellerNotificationsView: {e}")
            return Response({"success": False, "error": str(e)}, status=500)


# update reservation based on seller response (if approved, update the status to approved, if rejected, update the reservation)
class UpdateReservationView(APIView):
    def post(self, request, reservation_no):
        action = request.data.get("action")  # Expected values: 'approve' or 'reject'
        try:
            with connection.cursor() as cursor:
                if action == "approve":
                    cursor.execute("""
                        UPDATE reservation
                        SET Status = 'Approved'
                        WHERE Reservation_No = %s
                    """, [reservation_no])
                    return Response({"message": "Reservation approved successfully."}, status=status.HTTP_200_OK)
                
                elif action == "reject":
                    cursor.execute("""
                        UPDATE reservation
                        SET Status = 'Rejected'
                        WHERE Reservation_No = %s
                    """, [reservation_no])
                    return Response({"message": "Reservation rejected."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#display to buyer notifications
class BuyerNotificationsView(APIView):
    def get(self, request, buyer_id):
        try:
            with connection.cursor() as cursor:
                # Fetch reservations for the buyer where the status is 'Approved' or 'Rejected'
                cursor.execute("""
                    SELECT 
                        r.Reservation_No, 
                        r.Start_Date, 
                        r.End_Date, 
                        r.Status,
                        COALESCE(mv.Model, g.Gear_Name, sl.LAddress) AS item_name,
                        s.First_Name AS seller_first_name,
                        s.Last_Name AS seller_last_name
                    FROM reservation r
                    LEFT JOIN motorized_vehicle mv ON r.VIN = mv.VIN
                    LEFT JOIN gear g ON r.Product_No = g.Product_No
                    LEFT JOIN storage_lot sl ON r.Lot_No = sl.Lot_No
                    JOIN profile s ON r.Seller_ID = s.Profile_ID
                    WHERE r.Profile_ID = %s AND r.Status IN ('Approved', 'Rejected')
                """, [buyer_id])
                reservations = cursor.fetchall()

            # Map results to JSON format
            notifications = [
                {
                    "reservation_no": res[0],
                    "item_name": res[4] or "Unknown Item",
                    "start_date": res[1].strftime("%Y-%m-%d") if res[1] else None,
                    "end_date": res[2].strftime("%Y-%m-%d") if res[2] else None,
                    "status": res[3],
                    "seller_name": f"{res[5]} {res[6]}",
                }
                for res in reservations
            ]

            return Response({"success": True, "notifications": notifications}, status=200)
        except Exception as e:
            print(f"Error in BuyerNotificationsView: {e}")
            return Response({"success": False, "error": str(e)}, status=500)
        
# delete a reservation upon user acknowledge of rejection
class DeleteReservationView(APIView):
    def delete(self, request, reservation_no):
        try:
            with connection.cursor() as cursor:
                # Check if the reservation exists
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM reservation 
                    WHERE Reservation_No = %s
                """, [reservation_no])
                exists = cursor.fetchone()[0]

                if not exists:
                    return Response(
                        {"success": False, "message": "Reservation not found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Delete the reservation
                cursor.execute("""
                    DELETE FROM reservation 
                    WHERE Reservation_No = %s
                """, [reservation_no])

            return Response(
                {"success": True, "message": f"Reservation {reservation_no} deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# method for showing red dot on marketplace page
class CheckNotificationsView(APIView):
    def get(self, request, profile_id):
        try:
            with connection.cursor() as cursor:
                # Check for buyer notifications (status = Approved or Rejected)
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM reservation r
                    WHERE r.Profile_ID = %s AND r.Status IN ('Approved', 'Rejected')
                """, [profile_id])
                buyer_notifications = cursor.fetchone()[0]

                # Check for seller notifications (status = Pending Approval)
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM reservation r
                    WHERE r.Seller_ID = %s AND r.Status = 'Pending Approval'
                """, [profile_id])
                seller_notifications = cursor.fetchone()[0]

            # If either buyer or seller has notifications, return True
            has_notifications = buyer_notifications > 0 or seller_notifications > 0

            return Response({"success": True, "has_notifications": has_notifications}, status=200)
        except Exception as e:
            print(f"Error in CheckNotificationsView: {e}")
            return Response({"success": False, "error": str(e)}, status=500)



