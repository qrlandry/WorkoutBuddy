from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('user', views.UserView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('exercise', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercise/details/<int:pk>',
         views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('workout', views.WorkoutListCreateView.as_view(), name='workout_create'),
    path('workout/details/<int:pk>',
         views.WorkoutRetrieveUpdateDestroyView.as_view(), name='workout_destroy'),
    path('workout_exercise', views.WorkoutExerciseListCreateView.as_view(), name='workout_list'),
    path('workout_exercise/details/<int:pk>',
         views.WorkoutExerciseDetailView.as_view(), name='workout_detail'),
    path('workout_exercise_details', views.WorkoutExerciseDetailListCreateView.as_view(), name='workout_detail'),
    path('workout_exercise_details/details/<int:pk>',
         views.WorkoutExerciseDetailDetailView.as_view(), name='workout_detail_detail'),
    path('', views.home, name='home'),
    path('exercises/', views.exercise, name='exercise'),
    path('exercises_details/<str:pk>/', views.exercise_details, name='exercise_details'),
    path('create_exercise/', views.create_exercise, name='create_exercise'),
    path('login/', views.exercise, name='login'),
    path('register/', views.exercise, name='register'),
    path('sessions/', views.exercise, name='sessions'),
    path('log/', views.exercise, name='log'),
    path('profile/', views.exercise, name='profile'),
]