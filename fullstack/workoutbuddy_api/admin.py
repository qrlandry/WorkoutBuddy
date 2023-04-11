from django.contrib import admin
from .models import User, Exercise, Workout, WorkoutExerciseDetail, WorkoutExercise
# Register your models here.
admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutExerciseDetail)