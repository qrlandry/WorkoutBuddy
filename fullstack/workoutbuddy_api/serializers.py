from rest_framework import serializers
from .models import User, Exercise, Workout, WorkoutExercise, WorkoutExerciseDetail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'weight']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class ExerciseSerializer(serializers.ModelSerializer):
    body_part_display = serializers.CharField(source='get_body_part_display', read_only=True)
    equipment_display = serializers.CharField(source='get_equipment_display', read_only=True)

    class Meta:
        model = Exercise
        fields = ('id', 'body_part', 'body_part_display', 'equipment', 'equipment_display', 'name', 'description', 'user')
        read_only_fields = ('id', 'body_part_display', 'equipment_display')

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'status', 'name', 'created_at', 'workout_exercises']

    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(choices=Workout.STATUS_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(many=False)

    class Meta:
        model = WorkoutExercise
        fields = ['id', 'workout', 'exercise']

class WorkoutExerciseDetailSerializer(serializers.ModelSerializer):
    workout_exercise = WorkoutExerciseSerializer(many=False)

    class Meta:
        model = WorkoutExerciseDetail
        fields = ['id', 'workout_exercise', 'sets', 'reps', 'weight']