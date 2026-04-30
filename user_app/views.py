from rest_framework.authtoken.models import Token 
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework import status   


from user_app.models import User
from user_app.serializers import UserSerializer, UserAppSerializer

# Create your views here.
class UserAPIViews(APIView):
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()
    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=401)
        
        if request.user.role == 'employee':
            serializer = UserAppSerializer(request.user)
            return Response(serializer.data)
        
        elif request.user.role == 'admin':
            users = User.objects.all() #filter(is_superuser=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        
        return Response({"error": "Invalid user role."}, status=400)    
    
        
 
    def post(self, request):
        try:
            user_id = request.data.get('id')
            if user_id:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "User updated successfully", "data": serializer.data})
                        
            else: 
                
                serializer = UserSerializer(data=request.data)

                if serializer.is_valid(): 
                    serializer.save() 
                    if request.data.get('role') == 'admin' and not request.user.is_authenticated:
                        return Response({"error": "Only superuser can be created admin."}, status=403) 
                return Response({"message": "User created successfully", "data": serializer.data}) 
            
            return Response({"error": "Invalid data", "details": serializer.errors}, status=400)    
        except Exception as e:
            print("Error on creating user", e)
            return Response({"error": "An error occurred while creating the user."}, status=500)
        
    def delete(self, request):
        try:
            id = request.data.get('id')
            user = User.objects.filter(id=id).first()
            if not user:
                return Response({"error": "User not found."}, status=404)
            if request.user.role != 'admin':
                return Response({"error": "Only admin can delete users."}, status=403)
            user.delete()
            return Response({"message": "User deleted successfully."})
        except Exception as e:
            print("Error on deleting user", e)
            return Response({"error": "An error occurred while deleting the user."}, status=500)
        

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        #user = User.objects.filter(username=username).first()
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if not user:   
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({"error": "User account is disabled."}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful",
            "token": token.key,
            "user":{
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
        })

        
       