from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets, permissions
from .serializers import RegisterSerializer, LoginSerializer, TokenSerializer,MembershipSerializer,RolesSerializer, PaymentsSerializer, AnnouncementsSerializer, TransactionsSerializer
from rest_framework.authtoken.models import Token
from .models import Roles, Payments, Anouncements, Transactions, Membership


# Create your views here.

# view to register user
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': RegisterSerializer(user).data, 'token': TokenSerializer(token).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#view to login user
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'user': RegisterSerializer(user).data,
                             'token': TokenSerializer(token).data}, status=status.HTTP_200_OK)
        return Response({'detail': 'Credentials Invalid'}, status=status.HTTP_400_BAD_REQUEST)


# view for tokenretrieval 
class TokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                token_obj = Token.objects.get(key=token)
                return Response({'token': token_obj.key}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'detail' : 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail' : 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)
    

#view for membership
class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

#view for roles
class RolesViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer


#views for payments
class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

# view for announcements
class AnnouncementsViewSet(viewsets.ModelViewSet):
    queryset = Anouncements.objects.filter(active=True).order_by('-date')
    serializer_class = AnnouncementsSerializer

#view for transactions
class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Transactions.objects.all()
        return Transactions.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)