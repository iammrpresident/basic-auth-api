from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **credentials):
        email = credentials.get('email')
        password = credentials.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user and user.check_password(password):
                return user
            else:
                raise serializers.ValidationError(_("Invalid email or password."))
        else:
            raise serializers.ValidationError(_("Must include 'email' and 'password'."))
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        user =get_user_model()(**validated_data)
        
        if password:
            user.set_password(password)
            
        user.save()
        return user