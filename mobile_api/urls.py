from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.api_login, name='api_login'),
    path('register/', views.api_register, name='api_register'),
    path('predict/', views.api_predict, name='api_predict'),
]
