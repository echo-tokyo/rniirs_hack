"""
URL configuration for rniirs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from users.views import CustomUserAPIView
from news.views import NewsAPIView, CategoryAPIView, NewsParsAPIView, NewsFavoriteGETAPIView, NewsFavoritePOSTAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/users/', CustomUserAPIView.as_view(), name='users'),
    path('api/categories/', CategoryAPIView.as_view(), name='categories'),

    re_path(r'^api/news(/(?P<pk>\d+))?/?$', NewsAPIView.as_view(), name='news'),

    path('api/news/favorite/', NewsFavoriteGETAPIView.as_view()),
    # favorite param may be one of "like" ore "unlike"
    path('api/news/favorite/<int:pk>/<str:favorite>/', NewsFavoritePOSTAPIView.as_view()),

    path('api-dev/news/', NewsParsAPIView.as_view(), name='newspars'),
]
