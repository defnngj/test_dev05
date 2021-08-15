"""test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from demo_app import views
from api_app.views import ping
from rest_framework import routers, serializers, viewsets
from api_app.user_view import UserViewSet


# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', ping),
    path('hello/', views.hello),
    path('calculator/', views.calculator),
    path('demo/', include('demo_app.urls')),

    path('api/', include('api_app.urls')),

    path('rest/', include('rest_app.urls')),

    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
















