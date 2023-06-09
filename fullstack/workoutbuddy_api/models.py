from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Exercise(models.Model):
    TARGET_LOCATION = (
        ('Arms', 'Arms'),
        ('Shoulders', 'Shoulders'),
        ('Chest', 'Chest'),
        ('Core', 'Core'),
        ('Legs', 'Legs'),
        ('Back', 'Back'),
        ('Full body', 'Full Body')
    )

    EQUIPMENT = (
        ('Barbell', 'Barbell'),
        ('Dumbbell', 'Dumbbell'),
        ('Machine', 'Machine'),
        ('Bodyweight', 'Bodyweight'),
        ('Cardio', 'Cardio'),
        ('Other', 'Other'),
    )

    body_part = models.CharField(max_length=150, choices=TARGET_LOCATION)
    equipment = models.CharField(max_length=150, choices=EQUIPMENT)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=250, blank=True, null=True)
    photo_url = models.CharField(max_length=500, default='a string')
    user = models.ForeignKey(User, related_name="exercises", on_delete=models.CASCADE, blank=True, null=True)
    

    @classmethod
    def body_part_list(self):
        return [item[0] for item in self.TARGET_LOCATION]

    @classmethod
    def equipment_list(self):
        return [item[0] for item in self.EQUIPMENT]

    class Meta:
        unique_together = ('body_part', 'equipment', 'name')

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    STATUS_CHOICES = [
        ('Started', 'Started'),
        ('Finished', 'Finished'),
        ('Template', 'Template'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    name = models.CharField(max_length=150, default='string')
    date_completed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Workout(status={self.status} date={self.date_completed})"
    
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, related_name="workout_exercises", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"(workout={self.workout.user.username}, exercise={self.exercise.name})"
    
class WorkoutExerciseDetail(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, related_name="workout_exercise_details",
    on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    def __str__(self):
        return f"WorkoutExerciseDetail(workout_exercise={self.workout_exercise.exercise.name}, " \
               f"sets={self.sets}, reps={self.reps}, weight={self.weight})"

class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    goal_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.current_weight