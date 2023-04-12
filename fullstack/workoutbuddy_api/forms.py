from django.forms import ModelForm
from .models import Exercise
from django.contrib.auth.models import User

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ('name', 'body_part', 'equipment', 'description')

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
