from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class NewsAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        if request.query_params.get('confirmed') == "False" and request.user.is_superuser:
            news = News.objects.all().filter(is_confirmed=False)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)

        elif not request.query_params.get('user_id') == request.user.id:
            news = News.objects.all().filter(user_id=request.user.id)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)

        else:
            news = News.objects.all().filter(is_confirmed=True)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)

    @staticmethod
    def post(request):
        if request.user.is_superuser:
            serializer = NewsSerializer(data=request.data)
            serializer.is_confirmed = True

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = NewsSerializer(data=request.data)
            serializer.is_confirmed = False

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def patch(request):
        if request.user.is_superuser:
            news_id = request.query_params.get('news_id')

            if not news_id:
                return Response({'error': 'Missing news_id'}, status=status.HTTP_400_BAD_REQUEST)

            instance = get_object_or_404(News, pk=news_id)

            serializer = NewsSerializer(instance=instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request):
        if request.user.is_superuser:
            news_id = request.query_params.get('news_id')

            instance = get_object_or_404(News, pk=news_id)

            if not instance:
                return Response({'error': 'Missing news_id'}, status=status.HTTP_400_BAD_REQUEST)

            instance.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)