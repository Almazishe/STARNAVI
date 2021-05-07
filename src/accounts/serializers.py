from django.contrib.auth import get_user_model

from rest_framework import serializers


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