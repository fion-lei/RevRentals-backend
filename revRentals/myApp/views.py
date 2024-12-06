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
            
            # Check if the username already exists
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM profile WHERE Username = %s", [username])
                username_exists = cursor.fetchone()[0]

            if username_exists:
                print("Username exists already.")
                return Response({"error": "A profile with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)


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

class GetProfileIDView(APIView):
    def get(self, request, username):
        try:
            # Query to fetch profile_id using the username
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT Profile_ID
                    FROM profile
                    WHERE Username = %s
                """, [username])
                result = cursor.fetchone()

            if result:
                profile_id = result[0]
                return Response({
                    "success": True,
                    "profile_id": profile_id
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Profile not found for this username."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileDetailsView(APIView):
    def post(self, request):
        try:
            data = request.data
            profile_id = data.get('profile_id')
            
            print(f"Received profile_id: {profile_id}, type: {type(profile_id)}")
            
            # Convert profile_id to int if it's a string
            if isinstance(profile_id, str):
                profile_id = int(profile_id)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            license_number = data.get('license_number')
            address = data.get('address')

            with connection.cursor() as cursor:
                # First verify profile exists
                cursor.execute("SELECT COUNT(*) FROM profile WHERE Profile_ID = %s", [profile_id])
                exists = cursor.fetchone()[0]
                
                print(f"Profile exists: {exists}")
                
                if not exists:
                    return Response({
                        "success": False,
                        "error": f"Profile {profile_id} not found"
                    }, status=status.HTTP_404_NOT_FOUND)

                # Update profile
                cursor.execute("""
                    UPDATE profile 
                    SET First_Name = %s, Last_Name = %s, License = %s, Address = %s
                    WHERE Profile_ID = %s
                """, [first_name, last_name, license_number, address, profile_id])

                # Fetch updated data
                cursor.execute("""
                    SELECT Profile_ID, Username, First_Name, Last_Name, Email, License, Address, OverallRating
                    FROM profile 
                    WHERE Profile_ID = %s
                """, [profile_id])
                user = cursor.fetchone()
                
                print(f"Fetched user data: {user}")

                if user:
                    return Response({
                        "success": True,
                        "user": {
                            "profile_id": user[0],
                            "username": user[1],
                            "first_name": user[2],
                            "last_name": user[3],
                            "email": user[4],
                            "license": user[5],
                            "address": user[6],
                            "overall_rating": float(user[7]) if user[7] else None
                        }
                    }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in ProfileDetailsView: {str(e)}")
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)