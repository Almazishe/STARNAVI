from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import ActionLog

User = get_user_model()


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        _ = validated_data.pop("re_password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def validate(self, data):
        password = data.get('password')
        re_password = data.get('re_password')

        if password != re_password:
            raise serializers.ValidationError(
                {
                    "re_password": "Passwords don't match."
                }
            )

        return data

class ActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionLog
        fields = ('action_text', 'created_at')


class LastActivitySerializer(serializers.ModelSerializer):
    last_activities = serializers.SerializerMethodField('get_last_activities', read_only=True)
    last_request = serializers.SerializerMethodField('get_last_request', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_login', 'last_request', 'last_activities')
    
    def get_last_activities(self, obj):
        actions = ActionLog.objects.filter(user=obj).order_by('-created_at')
        serializer = ActionLogSerializer(actions, many=True)
        return serializer.data

    def get_last_request(self, obj):
        action = ActionLog.objects.filter(user=obj).order_by('-created_at').first()
        serializer = ActionLogSerializer(action)
        return serializer.data
