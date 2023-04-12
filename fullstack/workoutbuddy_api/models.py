from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    TARGET_LOCATION = (
        ('Arms', 'Arms'),
        ('Shoulers', 'Shoulders'),
        ('Chest', 'Chest'),
        ('Core', 'Core'),
        ('Legs', 'Legs'),
        ('Back', 'Back'),
        ('Full body', 'Full Body')
    )

    EQUIPMENT = (
        ('Barbell', 'Barbell'),
        ('Dumbell', 'Dumbell'),
        ('Machine', 'Machine'),
        ('Bodyweight', 'Bodyweight'),
        ('Cardio', 'Cardio'),
        ('Other', 'Other'),
    )

    body_part = models.CharField(max_length=150, choices=TARGET_LOCATION)
    equipment = models.CharField(max_length=150, choices=EQUIPMENT)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=250, blank=True, null=True)
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

    def __str__(self):
        return f"Workout(user={self.user.name} status={self.status})"
    
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
