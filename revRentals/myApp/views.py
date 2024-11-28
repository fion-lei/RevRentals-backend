from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from django.db import connection

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data  # DRF parses JSON data automatically
            username = data.get("username")
            password = data.get("password")
            print(username)
            print(password)

            # Query the database for the user
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Profile_ID, First_Name, Last_Name, Email, License, Username, Password, Address, OverallRating
                    FROM profile
                    WHERE Username = %s OR Email = %s
                """, [username, username])
                user = cursor.fetchone()

            if user:
                (profile_id, first_name, last_name, email, license, username,
                 hashed_password, address, overall_rating) = user

                # Validate the password
                if check_password(password, hashed_password):
                    return Response({
                        "success": True,
                        "message": "Login successful",
                        "user": {
                            "profile_id": profile_id,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "license": license,
                            "username": username,
                            "address": address,
                            "overall_rating": float(overall_rating) if overall_rating else None,
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        try:
            # Parse the incoming data
            data = request.data
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")

            # Check if the email already exists
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM profile WHERE Email = %s", [email])
                email_exists = cursor.fetchone()[0]

            if email_exists:
                print("email exists already.")
                return Response({"error": "A profile with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Hash the password
            hashed_password = make_password(password)

            # Insert the new profile
            with connection.cursor() as cursor:
                print("start")
                cursor.execute("""
                    INSERT INTO profile (First_Name, Last_Name, Email, License, Username, Password, Address, OverallRating)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [None, None, email, None, username, hashed_password, None, None])
                profile_id = cursor.lastrowid # Get the newly generated Profile_ID
            print("Profile created with ID:", profile_id)  # Debugging log


            garage_name = f"{username}_Garage"

            # Insert into the garage table
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO garage (Garage_Name, Profile_ID)
                    VALUES (%s, %s)
                """, [garage_name, profile_id])
                garage_id = cursor.lastrowid  # Get the newly generated Garage_ID
            print(garage_id)
        
            # Link the profile and garage in the `has` table
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO has (Profile_ID, Garage_ID)
                    VALUES (%s, %s)
                """, [profile_id, garage_id])
            print("Profile linked to garage in `has` table.")  # Debugging log

            # Return success response
            return Response({
                "success": True,
                "message": "Registration successful",
                "data": {
                    "profile_id": profile_id,
                    "garage_id": garage_id,
                    "garage_name": garage_name
                }
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class GetGarageIDView(APIView):
    def get(self, request, profile_id):
        try:
            # Query to fetch the garage_id associated with the profile_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT g.Garage_ID
                    FROM garage g
                    INNER JOIN has h ON g.Garage_ID = h.Garage_ID
                    WHERE h.Profile_ID = %s
                """, [profile_id])
                result = cursor.fetchone()

            if result:
                garage_id = result[0]
                return Response({"success": True, "garage_id": garage_id}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Garage not found for this profile."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)