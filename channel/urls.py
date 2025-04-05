from django.urls import path, include
from .views import RegisterView, LoginView, TokenView
from rest_framework.routers import DefaultRouter
from .views import MembershipViewSet, RolesViewSet,PaymentsViewSet, AnnouncementsViewSet, TransactionsViewSet





router = DefaultRouter()

router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'roles', RolesViewSet)
router.register(r'payments', PaymentsViewSet)
router.register(r'announcements', AnnouncementsViewSet)
router.register(r'transactions', TransactionsViewSet, basename='transactions')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenView.as_view(), name='token'),
    path('api/', include(router.urls)),






]