from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercise, name='exercise'),
    path('exercises_details/<str:pk>/', views.exercise_details, name='exercise_details'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('update_exercise/<str:pk>/', views.update_exercise, name='update_exercise'),
    path('delete_exercise/<str:pk>/', views.delete_exercise, name='delete_exercise'),
    path('exercises/', views.exercise, name='exercise'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('sessions/', views.exercise, name='sessions'),
    path('log/', views.log_start, name='log'),
    path('profile/', views.exercise, name='profile'),
]