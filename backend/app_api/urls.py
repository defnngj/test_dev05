from django.urls import path
from app_api.views.project_view import ProjectView

urlpatterns = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),
]
