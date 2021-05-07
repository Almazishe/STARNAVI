from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ActionLog
from .serializers import CreateUserSerializer

@api_view(['POST'])
def obtain_token(request):
    serializer = TokenObtainPairSerializer(data=request.data)
    
    if serializer.is_valid():
        ActionLog.act(serializer.user, f"Logined in")
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_create(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        ActionLog.act(user, "Registered")
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
