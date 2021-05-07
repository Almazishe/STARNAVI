from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from src.accounts.models import ActionLog
from .serializers import PostCreateSerializer, PostEvaluationSerializer


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated,])
@parser_classes([MultiPartParser, FormParser,])
def create_post(request):
    data = request.data

    serializer = PostCreateSerializer(data=data,context={'request': request})

    if serializer.is_valid():
        post = serializer.save()
        ActionLog.act(request.user, f"Created Post with title: {post.title}")
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
        elif user_post_like.unlike:
            message = f"Unliked Post: {user_post_like.post.title}"
        else:
            message = f"Removed Like or Dislike from Post: {user_post_like.post.title}"

        ActionLog.act(request.user, message)
        return Response({
            'success': message + " successfully."
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)