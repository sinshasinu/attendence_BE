
from rest_framework import serializers

from user_app.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta: 
        model = User 
        fields = '__all__'
    def create(self, validated_data):
        # Create a new user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        user.role = validated_data.get('role', 'employee') 
        user.phone_number = validated_data.get('phone_number') 
        user.department = validated_data.get('department')
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
class UserSerializerSafe(serializers.ModelSerializer):
    class Meta: 
        model = User 
        exclude = ["password", "is_superuser", "is_staff", "last_login", "groups", "user_permissions", "is_active", "date_joined"]

class UserAppSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta: 
        model = User 
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'department', 'token']
    def get_token(self, obj):
        try:
            token, created = Token.objects.get_or_create(user=obj)
            return f"Token {token.key}"
        except Exception as e:
            print("Error on getting token for user", obj, e)
            return ""
    
class UserDropdownSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ['id', 'username', 'department']