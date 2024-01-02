from .models import Profile
from .serializers import ProfileSerializer
from accounts.models import User
from accounts.permissions import IsVerified
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsVerified])
def get_user_profile_view(request):
    if request.method == 'GET':
        user = request.user
        profile = user.profile

        serializer = ProfileSerializer(profile)

        return Response(
            {
                'success':True,
                'profile':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_profile_view(request, user_id:str):
    if request.method == 'PATCH' or request.method == 'PUT':
        logged_in_user = request.user
        user = User.objects.get(id=user_id)

        if logged_in_user != user:
            return Response(
                {
                    'success':False,
                    'message':"You don't have the permission to update the user's profile!"
                }, status=status.HTTP_403_FORBIDDEN
            )

        profile = user.profile

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'Your profile has been successfully updated!',
                    'profile':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':True,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )
