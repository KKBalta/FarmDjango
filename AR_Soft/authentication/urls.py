from django.urls import path
from .views import RegisterView, PasswordResetRequestView, PasswordResetConfirmView, AddUserToGroupView, GroupListView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("password-reset-request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset-confirm/<str:token>/<int:user_id>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("add-user-to-group/", AddUserToGroupView.as_view(), name="add-user-to-group"),
    path("groups/", GroupListView.as_view(), name="group-list"),
]
