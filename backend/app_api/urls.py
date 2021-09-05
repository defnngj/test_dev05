from django.urls import path
from rest_framework import routers
from app_api.views.project_view import ProjectView
from app_api.views.module_view import ModuleView
from app_api.views.module_view import ModuleTreeView
from app_api.views.case_view import CaseViewSet


url_path = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),

    path('v1/module/', ModuleView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path("v1/module/tree/", ModuleTreeView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'v1/case', CaseViewSet)  # 用例管理

urlpatterns = url_path + router.urls

