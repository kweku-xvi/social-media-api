from .models import LikePost, LikeComment
from accounts.permissions import IsVerified
from comments.models import Comment
from django.shortcuts import render
from posts.models import Post
from rest_framework import  status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


def get_post(post_id:str):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {
                'success':True,
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


@api_view(['POST'])
@permission_classes([IsVerified])
def like_post_view(request, post_id:str):
    if request.method == 'POST':
        user = request.user
        post = get_post(post_id=post_id)

        if LikePost.objects.filter(user=user, post=post).exists():
            return Response(
                {
                    'success':False,
                    'message':'You have already liked this post'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        like = LikePost.objects.create(
            user=user,
            post=post
        )

        return Response(
            {
                'success':True,
                'message':'You have liked the post!'
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def unlike_post_view(request, post_id:str):
    if request.method == 'DELETE':
        user = request.user
        post = get_post(post_id=post_id)

        if not LikePost.objects.filter(user=user, post=post).exists():
            return Response(
                {
                    'success':False,
                    'message':'You have not liked this post'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        like = LikePost.objects.get(user=user, post=post)
        like.delete()

        return Response(
            {
                'success':True,
                'message':'You have unliked this post!'
            }, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsVerified])
def like_comment_view(request, comment_id:str):
    if request.method == 'POST':
        user = request.user
        comment = get_comment(comment_id=comment_id)

        if LikeComment.objects.filter(user=user, comment=comment).exists():
            return Response(
                {
                    'success':False,
                    'message':'You have already liked this comment'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        like = LikeComment.objects.create(
            user=user,
            comment=comment
        )

        return Response(
            {
                'success':True,
                'message':'You have liked the comment!'
            }, status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def unlike_comment_view(request, comment_id:str):
    if request.method == 'DELETE':
        user = request.user
        comment = get_comment(comment_id=comment_id)

        if not LikeComment.objects.filter(user=user, comment=comment).exists():
            return Response(
                {
                    'success':False,
                    'message':'You have not liked this comment'
                }, status=status.HTTP_400_BAD_REQUEST
            )

        comment = LikeComment.objects.get(user=user, comment=comment)
        comment.delete()

        return Response(
            {
                'success':True,
                'message':'You have unliked this comment!'
            }, status=status.HTTP_200_OK
        )