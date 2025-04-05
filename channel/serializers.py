from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from .models import Membership, Roles, Payments, Anouncements, Transactions, CustomUser

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
    password = serializers.CharField(write_only=True)
    

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            return user
        raise serializers.ValidationError('Credentials Invalid')
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

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


#serializing the payments model
class PaymentsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    Membership = serializers.PrimaryKeyRelatedField(queryset=Membership.objects.all())

    class Meta:
        model = Payments
        fields = ['user', 'membership', 'amount', 'payment_date', 'payment_type']


#serializing the announcements model 
class AnnouncementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anouncements
        fields = ['id', 'title', 'content', 'date', 'active']

# serializer for transactions
class TransactionsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transactions
        fields = ['id', 'user', 'amount', 'payment_method', 'payment_date', 'reference_id', 'description']
        read_only_fields = ['user', 'payment_date']

