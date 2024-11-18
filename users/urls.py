from django.urls import path
from users.views import (
    RegisterAPIView,
    LoginAPIView,
    UserListView,
    UserCountView,
    UserProfileView,
    LogoutView, ChangePasswordView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('all-users/', UserListView.as_view(), name='user-list'),
    path('user-count/', UserCountView.as_view(), name='user-count'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
