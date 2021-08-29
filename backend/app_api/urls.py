from django.urls import path
from app_api.views.project_view import ProjectView
from app_api.views.module_view import ModuleView


urlpatterns = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),

    path('v1/module/', ModuleView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
]
