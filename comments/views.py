from .models import Comment
from .serializers import CommentSerializer
from accounts.models import User
from accounts.permissions import IsVerified
from django.shortcuts import render
from posts.models import Post
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

def get_post(post_id:str):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {
                'success':False,
                'message':'Post does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return post

def get_comment(comment_id:str):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {
                'success':True,
                'message':'Comment does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return comment


def get_user(uid:str):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response(
            {
                'success':True,
                'message':'User does not exist'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    return user

@api_view(['POST'])
@permission_classes([IsVerified])
def add_comment_view(request, post_id:str):
    if request.method == 'POST':
        user = request.user
        post = get_post(post_id=post_id)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post, user=user)

            return Response(
                {
                    'success':True,
                    'comment':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'comment':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_specific_comment_view(request, comment_id:str):
    if request.method == 'GET':
        comment = get_comment(comment_id=comment_id)
        serializer = CommentSerializer(comment)

        return Response(
            {
                'success':True,
                'comment':serializer.data
            }, status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes([IsVerified])
def get_comments_on_post_view(request, post_id:str):
    if request.method == 'GET':
        post = get_post(post_id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                'success':True,
                'comments':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_comments_by_user_view(request, uid:str):
    if request.method == 'GET':
        user = get_user(uid=uid)
        comments = Comment.objects.filter(user=user)
        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                'success':True,
                'comments':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def delete_comment_view(request, comment_id:str):
    if request.method == 'DELETE':
        user = request.user
        comment = get_comment(comment_id=comment_id)

        if user != comment.user and user != comment.post.user and not user.is_staff:
            return Response(
                {
                    'success':True,
                    'message':'You do not have the permission to delete this comment!'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        comment.delete()

        return Response(
            {
                'success':True,
                'message':'Comment has been successfully deleted!'
            }, status=status.HTTP_204_NO_CONTENT
        )