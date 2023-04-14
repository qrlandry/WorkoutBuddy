from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercises/', views.exercise, name='exercise'),
    path('exercises_details/<str:pk>/', views.exercise_details, name='exercise_details'),
    path('workout_exercises_details/<str:pk>/', views.workout_exercise_details, name='workout_exercise_details'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('update_exercise/<str:pk>/', views.update_exercise, name='update_exercise'),
    path('delete_exercise/<str:pk>/', views.delete_exercise, name='delete_exercise'),
    path('delete_workout/<str:pk>/', views.delete_workout, name='delete_workout'),
    path('exercises/', views.exercise, name='exercise'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('sessions/', views.sessions, name='sessions'),
    path('workout_details/<int:workout_id>', views.workout_details, name='workout_details'),
    path('log/', views.log, name='log'),
    path('log_start/', views.log_start, name='log_start'),
    path('add_workout_exercises/<int:workout_id>/', views.add_exercise, name='add_workout'),
    path('log_end/<int:workout_id>/', views.log_end, name='log_end'),
    path('edit_profile/', views.edit_profile, name='edit_user_profile'),
    path('profile/', views.profile, name='user_profile'),
]