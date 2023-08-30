from .models import *
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email','username', 'password', 'password2','otp']
        extra_kwargs ={
            'password': {
                'write_only':True
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('passwords did not match')
        if not attrs.get('username'):
            raise serializers.ValidationError("field username is required")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ['email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password',"otp",
    "email_token",
    "forget_password",
    "is_active",
    "is_admin",]
        
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style= {'input_type':'password'},write_only = True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('passwords did not match')
        user.set_password(password)
        user.save()
        return attrs
    