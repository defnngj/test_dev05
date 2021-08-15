from django.urls import path, include
from rest_app import views


urlpatterns = [
    path('v1/hello/', views.hello),
    path('v1/user/', views.UserView.as_view()),
    path('v1/user/<int:uid>/', views.UserView.as_view()),
    path('v1/user2/', views.user_view),
]
