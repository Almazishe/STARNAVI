from datetime import timedelta

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from src.accounts.models import ActionLog
from .serializers import (
    PostCreateSerializer, 
    PostEvaluationSerializer, 
    PostAnalysisSerializer,
    ByDateLikesAnalysisSerializer,
    DateRangeSerializer
)
from .models import Post, UserPostLike



@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
@parser_classes([MultiPartParser, FormParser,])
def create_post(request):
    data = request.data

    serializer = PostCreateSerializer(data=data,context={'request': request})

    if serializer.is_valid():
        post = serializer.save()
        ActionLog.act(request.user, ActionLog.CREATE_POST, f"Created Post with title: {post.title}")
        return Response({
            "success": "Post created successfully."
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
def evaluate_post(request):
    data = request.data

    serializer = PostEvaluationSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        user_post_like = serializer.save()

        if user_post_like.like:
            message = f"Liked Post: {user_post_like.post.title}"
            ActionLog.act(request.user, ActionLog.LIKE, message)
        elif user_post_like.unlike:
            message = f"Unliked Post: {user_post_like.post.title}"
            ActionLog.act(request.user, ActionLog.UNLIKE, message)
        else:
            message = f"Removed Like or Dislike from Post: {user_post_like.post.title}"
            ActionLog.act(request.user, ActionLog.REMOVE_LIKE, message)

        return Response({
            'success': message + " successfully."
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_posts_analytics(request):
    """
    Shows total number of likes and dislikes of post
    in given period of time
    """
    
    posts = Post.objects.all()
    serializer = PostAnalysisSerializer(posts, many=True, context={'request': request})
    ActionLog.act(request.user, ActionLog.GET, "Get the posts anaylitics")

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_likes_analysis(request):
    dates_serializer = DateRangeSerializer(data=request.GET)
    if dates_serializer.is_valid():

        # Collect all dates between date_from and date_to inclusive
        date_from = dates_serializer.validated_data['date_from']
        date_to = dates_serializer.validated_data['date_to']
        delta = timedelta(days=1)
        dates = []
        while date_from <= date_to:
            dates.append({
                'date': date_from
            })
            date_from += delta

        serializer = ByDateLikesAnalysisSerializer(data=dates, many=True)
        if serializer.is_valid():
            ActionLog.act(request.user, ActionLog.GET, "Get the posts likes anaylitics")
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(dates_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        