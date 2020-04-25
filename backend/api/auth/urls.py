from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import *

app_name = 'auth'

urlpatterns = [
    path('login', obtain_jwt_token),
    path('refresh_token', refresh_jwt_token),
    path('register', CreateUser.as_view()),
]