from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.pagination import PageNumberPagination


from users.serializers import CustomUserSerializer
from .serializers import *
from .models import *


class CategoryAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

class OneNewsAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request, pk):
        news = News.objects.get(pk=pk)

        if not news.is_confirmed and not request.user.is_superuser:
            return Response({'error': 'news was not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news, many=False)
        return Response(serializer.data)


class NewsAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        # Создаем пагинатор
        paginator = PageNumberPagination()
        paginator.page_size = 20  # Дефолтный размер страницы
        paginator.page_size_query_param = 'page_size'  # Параметр для изменения размера

        # Основная логика фильтрации
        if not request.query_params:
            news = News.objects.filter(is_confirmed=True)

        elif request.query_params.get('confirmed') == "False" and request.user.is_superuser:
            news = News.objects.filter(is_confirmed=False)

        elif request.query_params.get('user_id') == str(request.user.id):
            news = News.objects.filter(author_id=request.user.id)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Применяем пагинацию к queryset
        paginated_news = paginator.paginate_queryset(news, request)

        # Сериализация + возврат с метаданными пагинации
        serializer = NewsSerializer(paginated_news, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    def post(request):
        if request.user.is_superuser:
            data = request.data
            data["is_confirmed"] = True
            serializer = NewsSerializer(data=data)
            if serializer.is_valid():
                serializer.save(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            serializer = NewsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(request.data)
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

            data = request.data
            data["is_confirmed"] = True
            serializer = NewsSerializer(instance=instance, data=data, partial=True)

            if serializer.is_valid():
                serializer.update(instance, data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

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
            return Response(status=status.HTTP_403_FORBIDDEN)


class NewsParsAPIView(APIView):

    @staticmethod
    def post(request):

        serializer = NewsParsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsShortAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        # Создаем пагинатор
        paginator = PageNumberPagination()
        paginator.page_size = 20  # Дефолтный размер страницы
        paginator.page_size_query_param = 'page_size'  # Параметр для изменения размера

        # Основная логика фильтрации
        if not request.query_params:
            news = News.objects.filter(is_confirmed=True)

        elif request.query_params.get('confirmed') == "False" and request.user.is_superuser:
            news = News.objects.filter(is_confirmed=False)

        elif request.query_params.get('user_id') == str(request.user.id):
            news = News.objects.filter(author_id=request.user.id)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Применяем пагинацию к queryset
        paginated_news = paginator.paginate_queryset(news, request)

        # Сериализация + возврат с метаданными пагинации
        serializer = NewsShortSerializer(paginated_news, many=True)
        return paginator.get_paginated_response(serializer.data)



class NewsFavoriteGETAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        str_user_id = request.query_params.get('user_id')

        if not str_user_id:
            # get favorite news for current user
            news = News.objects.all().filter(is_confirmed=True, liked=request.user)
            serializer = NewsSerializer(news, many=True)
            user_serializer = CustomUserSerializer(request.user, many=False)
            return Response({"news": serializer.data, "user": user_serializer.data})

        # get favorite news for specified user
        try:
            user_id = int(str_user_id)
        except ValueError as err:
            return Response({"error": "invalid user id was given"}, status=status.HTTP_400_BAD_REQUEST)
        user_with_favorite = get_object_or_404(CustomUser, pk=user_id)
        user_serializer = CustomUserSerializer(user_with_favorite, many=False)

        news = News.objects.all().filter(is_confirmed=True, liked=user_with_favorite)
        serializer = NewsSerializer(news, many=True)
        return Response({"news": serializer.data, "user": user_serializer.data})

class NewsFavoritePOSTAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    @staticmethod
    def patch(request, pk, favorite):
        instance = get_object_or_404(News, pk=pk)

        if favorite == "like":
            instance.liked.add(request.user)
        elif favorite == "unlike":
            instance.liked.remove(request.user)
        else:
            return Response({"error": "invalid favorite path param was given"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = NewsSerializer(instance=instance, data={}, partial=True)

        if serializer.is_valid():
            serializer.update(instance, {})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
