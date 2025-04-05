from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)

    def save(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance


class NewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    date = serializers.DateField(required=False)
    category_id = serializers.IntegerField()
    is_confirmed = serializers.BooleanField(default=False, required=False)
    author_id = serializers.IntegerField()

    def save(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save()
        return instance

