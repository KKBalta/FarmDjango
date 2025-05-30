from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.serializers import Serializer, CharField, EmailField, ValidationError, BooleanField
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
import logging
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Configure logger
logger = logging.getLogger(__name__)


class EmailTokenObtainSerializer(AuthTokenSerializer):
    username = None
    email = EmailField(required=True)
    password = CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Find the user with this email
            try:
                user = User.objects.get(email=email)
                # Use the username for authentication
                user = authenticate(request=self.context.get('request'),
                                   username=user.username,
                                   password=password)
            except User.DoesNotExist:
                user = None

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmailTokenObtainView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class RegisterSerializer(Serializer):
    username = CharField(required=True)  # Add username field
    email = EmailField(required=True)
    password = CharField(required=True, write_only=True)
    password_confirmation = CharField(required=True, write_only=True)
    acceptTerms = BooleanField(required=True, write_only=True)

    def validate(self, data):
        logger.info(f"RegisterSerializer validation started with data: {data.keys()}")
        
        # Check if required fields exist
        for field in ['username', 'email', 'password', 'password_confirmation', 'acceptTerms']:
            if field not in data:
                logger.error(f"Field '{field}' missing from registration data")
                raise ValidationError({field: f"This field is required."})
        
        # Check if passwords match
        if data['password'] != data['password_confirmation']:
            logger.warning(f"Password mismatch for email: {data.get('email')}")
            raise ValidationError({"password": "Passwords do not match."})
        
        # Check if user accepted terms - simplified as it's now a proper boolean
        logger.debug(f"acceptTerms value: {data['acceptTerms']} (type: {type(data['acceptTerms']).__name__})")
        if not data['acceptTerms']:
            logger.warning(f"Terms not accepted by email: {data.get('email')}")
            raise ValidationError({"acceptTerms": "You must accept the terms and conditions."})
        
        # Check if email already exists
        email = data['email']
        if User.objects.filter(email=email).exists():
            logger.warning(f"Email already exists: {email}")
            raise ValidationError({"email": "A user with this email already exists."})
        
        # Check if username already exists
        username = data['username']
        if User.objects.filter(username=username).exists():
            logger.warning(f"Username already exists: {username}")
            raise ValidationError({"username": "This username is already taken."})
        
        return data

    def create(self, validated_data):
        logger.info(f"Creating user with username: {validated_data.get('username')}, email: {validated_data.get('email')}")
        
        # Remove fields not used in User.create_user
        validated_data.pop('password_confirmation', None)
        validated_data.pop('acceptTerms', None)
        
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            logger.info(f"User created successfully with ID: {user.id}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        logger.info(f"Registration attempt received with data keys: {request.data.keys()}")
        
        # Log content type and headers for debugging
        logger.debug(f"Content-Type: {request.content_type}")
        logger.debug(f"Request headers: {request.headers}")
        
        # Log request data
        try:
            logger.info(f"Registration data username: {request.data.get('username', 'Not provided')}")
            logger.info(f"Registration data email: {request.data.get('email', 'Not provided')}")
            # Don't log passwords!
            logger.info(f"acceptTerms value: {request.data.get('acceptTerms', 'Not provided')}")
        except Exception as e:
            logger.warning(f"Could not log request data: {str(e)}")
        
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            logger.info("Registration data validation successful")
            
            try:
                user = serializer.save()
                logger.info(f"User saved with ID: {user.id}, Username: {user.username}")
                
                # Create an auth token for the new user
                try:
                    token = Token.objects.create(user=user)
                    logger.info(f"Auth token created successfully for user: {user.username}")
                except Exception as token_error:
                    logger.error(f"Failed to create auth token: {str(token_error)}")
                    # Continue anyway, token is not critical for registration
                    token = None
                
                response_data = {
                    "message": "User registered successfully!",
                    "email": user.email,
                    "username": user.username,
                }
                
                if token:
                    response_data["token"] = token.key
                    response_data["userId"] = user.id
                
                logger.info(f"Registration successful for user: {user.username}")
                return Response(response_data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                return Response({"error": "Registration failed due to an unexpected error."}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Registration validation failed: {serializer.errors}")
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


class UserDetailView(APIView):
    """
    Endpoint to retrieve the currently authenticated user's details
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"User detail request for user: {request.user.username} (ID: {request.user.id})")
        
        # Log authentication method
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        logger.debug(f"Authentication header: {auth_header[:10]}... (truncated)")
        
        try:
            serializer = UserSerializer(request.user)
            logger.info(f"User details successfully serialized for user: {request.user.username}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving user details: {str(e)}")
            return Response({"error": "Failed to retrieve user details"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)