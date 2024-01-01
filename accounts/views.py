import os, jwt
from .models import User
from .permissions import IsVerified
from .serializers import SignUpSerializer, LoginSerializer, UsersSerializer
from .utils import send_verification_email, send_password_reset_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()


@api_view(['POST'])
def sign_up_view(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            user = User.objects.get(email=serializer.validated_data['email'])
            token = RefreshToken.for_user(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('verify_user')
            absolute_url = f'http://{current_site}{relative_link}?token={token}'
            link = str(absolute_url)
            send_verification_email(email=user.email, username=user.username, link=link)

            return Response(
                {
                    'success':True,
                    'message':'User has been successfully created. Verify your email',
                    'user':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )
        

@api_view(['GET'])
def verify_user_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified=True
                user.save()
            
            return Response(
                {
                    'success':True,
                    'message':'Account has been successfully verified!'
                }, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as e:
            return Response(
                {
                    'success':False,
                    'message':'Activation link expired'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as e:
            return Response(
                {
                    'success':False,
                    'message':'Invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidTokenError as e:
            return Response(
                {
                    'success':False,
                    'message':'invalid token'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist as e:
            return Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':False,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            tokens = serializer.generate_jwt_tokens(serializer.validated_data)

            return Response(
                {
                    'success':True,
                    'message':'Login successful!',
                    'tokens':tokens
                }, status=status.HTTP_200_OK
            )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_users_view(request):
    if request.method == 'GET':
        user = request.user

        if not user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'Only admin users have the permission to perform this action!'
                }, status=status.HTTP_403_FORBIDDEN
            ) 
        
        all_users = User.objects.all()
        serializer = UsersSerializer(all_users, many=True)

        return Response (
            {
                'success':True,
                'users':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
def password_reset_view(request):
    if request.method == 'POST':
        email = request.data.get('email')

        if not email:
            return Response (
                {
                    'success':False,
                    'message':'Email is required'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request).domain
            relative_link = reverse('password_reset_confirm')
            absolute_url = f'http://{current_site}{relative_link}?uid={uid}&token={token}'
            link = str(absolute_url)
            send_password_reset_mail(email=user.email, username=user.username, link=link)

            return Response(
                {
                    'success':True,
                    'message':'Password reset mail has been successfully sent!'
                }, status=status.HTTP_200_OK
            )

        except User.DoesNotExist as e:
            return Response(
                {
                    'success':True,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':True,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['PATCH'])
def password_reset_confirm_view(request):
    if request.method == 'PATCH':
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return Response(
                {
                    'success':False,
                    'message':'All fields are required!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(id=user_id)

            if not default_token_generator.check_token(user, token):
                return Response(
                    {
                        'success':False,
                        'message':'Invalid token'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(password)
            user.save()
            
            return Response(
                {
                    'success':True,
                    'message':'Password reset successful!'
                }, status=status.HTTP_200_OK
            )       
        except User.DoesNotExist as e:
            return Response(
                {
                    'success':True,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'success':True,
                    'message':str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([IsVerified])
def search_user_view(request):
    if request.method == 'GET':
        username = request.query_params.get('username')

        if not username:
            return Response(
                {
                    'success':True,
                    'message':'Please provide a search query'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(
            Q(username__icontains=username)
        )

        serializer = UsersSerializer(users, many=True)

        return Response(
            {
                'success':True,
                'message':'Search results:',
                'users':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_user_details_view(request, user_id:str):
    if request.method == 'PUT' or request.method == 'PATCH':
        logged_in_user = request.user

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {
                    'success':False,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if logged_in_user != user and not logged_in_user.is_staff:
            return Response(
                {
                    'success':True,
                    'message':'You do not have the permission to update user details'
                }, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UsersSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'User details have been successfully updated!',
                    'user':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_200_OK
        )