from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
from rest_framework.permissions import AllowAny


class RegisterSerializer(Serializer):
    username = CharField(required=True)
    email = EmailField(required=True)
    password = CharField(required=True, write_only=True)
    confirm_password = CharField(required=True, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({"username": "A user with this username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"email": "A user with this email already exists."})
        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)  # Generate secure token
            reset_link = request.build_absolute_uri(
                reverse('password-reset-confirm', kwargs={'token': token, 'user_id': user.id})
            )
            # Send email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@example.com',
                [email],
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email address."}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token, user_id):
        # Step 1: Find the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Validate the token
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Validate passwords
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 4: Update the password
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)


class AddUserToGroupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        group_name = request.data.get('group')

        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            return Response({"message": f"User {username} added to group {group_name}."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        

class GroupListView(APIView):
    def get(self, request):
        groups = Group.objects.all().values("id", "name")  # Fetch all groups
        return Response(groups, status=status.HTTP_200_OK)