from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class NotificationsView(APIView):
    def get(self, request, profile_id):
        """Fetch notifications for a user"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Notification_ID, Type, Message, Created_At, Is_Read, Reservation_No
                    FROM notifications
                    WHERE Profile_ID = %s AND Is_Read = FALSE
                    ORDER BY Created_At DESC
                """, [profile_id])
                
                notifications = []
                for row in cursor.fetchall():
                    notifications.append({
                        'id': row[0],
                        'type': row[1],
                        'message': row[2],
                        'created_at': row[3].isoformat(),
                        'is_read': row[4],
                        'reservation_no': row[5]
                    })
                
                return Response({'notifications': notifications}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, notification_id):
        """Mark a notification as read"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE notifications
                    SET Is_Read = TRUE
                    WHERE Notification_ID = %s
                """, [notification_id])
                
                return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)