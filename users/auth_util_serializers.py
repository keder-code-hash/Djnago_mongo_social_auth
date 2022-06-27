from .models.Users import Users
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import password_validation 
from django.utils.translation import gettext_lazy as _

from .serializers.UsersSerializers import UsersModelSerailizers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = Users
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer): 
    email = serializers.CharField(max_length = 255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    user = UsersModelSerailizers(read_only = True)
    tokens = serializers.SerializerMethodField() 

    def get_tokens(self, obj):
        user = Users.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        } 
 
     
    def validate(self,attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = Users.objects.filter(email=email)
        # print(email)
        # user = auth.authenticate(username=username, password=password)

        user = auth.authenticate(email=email, password=password)
        # if Users.objects.get(email= email).check_password(password):
        #     user = Users.objects.get(email= email)

        if filtered_user_by_email.exists() == False:
            raise AuthenticationFailed(
                detail='Invalid email id. Please check it out.')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')

        return { 
            'email': user.email,
            'user':user,
            # 'tokens': user.tokens
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    } 


class ResetPasswordEmailSentSerializers(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        field = ['email']


class ResetPasswordSerializers(serializers.Serializer):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
        "password_requirements" : _("Password did not match with minimum password validation Requirements")
    }
    new_password1 = serializers.CharField(max_length = 200 )
    new_password2 = serializers.CharField(max_length = 200 )
 
    def validate(self, attrs):
        try:
            password_validation.validate_password(attrs.get("new_password1"))
            if attrs.get("new_password1") and attrs.get("new_password2") : 
                if attrs.get("new_password1") != attrs.get("new_password2"):
                    raise serializers.ValidationError(self.error_messages.get("password_mismatch"))
            return attrs  
        except:
            raise serializers.ValidationError(self.error_messages.get("password_requirements"))
        

    def save(self,user):
        password = self.validated_data.get("new_password1")
        user.set_password(password)
        user.save()
        return user