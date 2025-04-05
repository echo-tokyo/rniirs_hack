from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    login = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(write_only=True, default=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance
