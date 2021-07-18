from django.urls import path, include
from demo_app import calculator_api


urlpatterns = [
    path('add/', calculator_api.add),
]
