from django.urls import path
from .views import RegisterView, LoginView, TokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenView.as_view(), name='token'),










]