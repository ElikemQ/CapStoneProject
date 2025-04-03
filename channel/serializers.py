from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import Membership, Roles

class CustomUserSeriailizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only' : True}}

    def create(self,validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.Charfield(write_only=True)
    

    def validate(self, data):
        user = get_user_model().objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError('Credentials Invalid')
    

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model =Token
        fields = ['key']


# serializing membership model
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['user', 'start_date', 'end_date', 'membership_type']


# serializing the roles model
class RolesSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), many=True)

    class Meta:
        model = Roles
        fields = ['id', 'name', 'description', 'users']
