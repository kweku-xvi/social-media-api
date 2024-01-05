from .models import FollowUser
from accounts.models import User
from accounts.permissions import IsVerified
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def get_user(uid:str):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response(
            {
                'success':False,
                'message':'User does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return user


@api_view(['POST'])
@permission_classes([IsVerified])
def follow_user_view(request, uid:str):
    if request.method == 'POST':
        user = request.user
        following = get_user(uid=uid) # account following

        if user == following:
            return Response(
                {
                    'success':False,
                    'message':'You can not follow your own account'
                }, status=status.HTTP_403_FORBIDDEN
            )

        if FollowUser.objects.filter(user=following, follower=user).exists():
            return Response(
                {
                    'success':False,
                    'message':'You are already following this user'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        follow = FollowUser.objects.create(user=following, follower=user)

        return Response(
            {
                'success':True,
                'message':f'You are now following {follow.user.username}'
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def unfollow_user_view(request, uid:str):
    if request.method == 'DELETE':
        user = request.user
        following = get_user(uid=uid) # account following

        if user == following:
            return Response(
                {
                    'success':False,
                    'message':'You can not unfollow your own account'
                }, status=status.HTTP_403_FORBIDDEN
            )

        if not FollowUser.objects.filter(user=following, follower=user).exists():
            return Response(
                {
                    'success':False,
                    'message':'You are not following this user'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        follow = FollowUser.objects.get(user=following, follower=user)
        follow.delete()

        return Response(
            {
                'success':True,
                'message':f'You have unfollowed {follow.user.username}'
            }, status=status.HTTP_200_OK
        )