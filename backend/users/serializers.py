from rest_framework import serializers

from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    login = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(read_only=True, default=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # Создаем стандартный токен

        # Добавляем пользовательские поля
        token["is_superuser"] = user.is_superuser

        return token
