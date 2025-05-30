from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    RegisterView, PasswordResetRequestView, PasswordResetConfirmView, 
    AddUserToGroupView, GroupListView, UserDetailView, EmailTokenObtainView
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset-request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset-confirm/<str:token>/<int:user_id>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("add-user-to-group/", AddUserToGroupView.as_view(), name="add-user-to-group"),
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    path("login/", EmailTokenObtainView.as_view(), name="api-email-token-auth"),
]
