from .models import Post
from .serializers import PostSerializer
from accounts.models import User
from accounts.permissions import IsVerified
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def get_post(id:str):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(
            {
                'success':False,
                'message':'Post does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return post


@api_view(['POST'])
@permission_classes([IsVerified])
def create_post_view(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                {
                    'success':True,
                    'post':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_specific_post_view(request, id:str):
    if request.method == 'GET':
        post = get_post(id=id)
        serializer = PostSerializer(post)

        return Response(
            {
                'success':True,
                'post':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_posts_by_user_view(request, uid:str):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response(
                {
                    'success':True,
                    'message':'User does not exist'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)

        return Response(
            {
                'success':True,
                'message':f'Posts by {user.username}',
                'posts':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def search_posts_view(request):
    if request.method == 'GET':
        query = request.query_params.get('query')

        if not query:
            return Response(
                {
                    'success':True,
                    'message':'Please provide a search query!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        posts = Post.objects.filter(text__icontains=query)
        serializer = PostSerializer(posts, many=True)

        return Response(
            {
                'success':True,
                'message':'Search results below:',
                'posts':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def delete_post_view(request, id:str):
    if request.method == 'DELETE':
        user = request.user
        post = get_post(id=id)

        if user != post.user and not user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You do not have the permission to delete this post!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        post.delete()

        return Response(
            {
                'success':True,
                'message':'The post has been successfully deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )