from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView,ItemCreateView,ItemDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('items/', ItemCreateView.as_view(), name='item-list-create'),
    path('items/<int:item_id>/', ItemDetailView.as_view(), name='item-detail'),
]