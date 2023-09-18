# tracks 
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    '''
    User Model Serializer
    '''
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        else:
            raise serializers.ValidationError('password cannot be empty')
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    '''
    Login Serializer
    '''

    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password :
            user = authenticate(
                request = self.context.get('request'),
                email = email,
                password = password
            )
            if not user:
                raise serializers.ValidationError('Invalid Credentials')
        else:
            raise serializers.ValidationError('Invalid Credentials')
        
        attrs['user'] = user

        return attrs

class RegisterSerializer(serializers.ModelSerializer):
    '''
    Registeration Serializer
    '''
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only = True,
        required= True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(
        write_only = True,
        required= True
    )
    name = serializers.CharField(required=True)
    alias = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'name', 'alias')

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError('Password and Password2 doesn\'t match')
        else:
            user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
            )
            user.save()
            return user
