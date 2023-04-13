from django.shortcuts import render, redirect
from .models import Exercise, Workout, WorkoutExercise, WorkoutExerciseDetail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .forms import ExerciseForm, UserUpdateForm
from django.utils import timezone

# login the user
def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page} 
    return render(request, 'login_register.html', context)

# logout the user
def logout_user(request):
    logout(request)
    return redirect('home')

# register the user
def register_user(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            auth_login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An error occured during registration')

    return render(request, 'login_register.html', {'form': form})

# render the homepage
def home(request):
    return render(request, 'home.html')

# render out the exercises with searchbar and filters
@login_required(login_url='login/')
def exercise(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    body_part = request.GET.get('body_part') if request.GET.get('body_part') != None else ''
    equipment = request.GET.get('equipment') if request.GET.get('equipment') != None else ''

    exercises = Exercise.objects.all()

    if q:
        exercises = exercises.filter(name__icontains=q)

    if body_part:
        exercises = exercises.filter(body_part=body_part)
    
    if equipment:
        exercises = exercises.filter(equipment=equipment)

    context = { 'exercises': exercises }
    return render(request, 'exercise.html', context)

# exercise details page
@login_required(login_url='login/')
def exercise_details(request, pk):
    exercise = Exercise.objects.get(id=pk)
    context = {'exercise': exercise}
    return render(request, 'exercise_details.html', context)

# view exercise details page from workout sessions
@login_required(login_url='login/')
def workout_exercise_details(request, pk):
    workout_exercise = WorkoutExercise.objects.get(id=pk)
    exercise = workout_exercise.exercise
    context = {'exercise': exercise}
    return render(request, 'exercise_details.html', context)

# exercise create method
@login_required(login_url='login/')
def create_exercise(request):
    form = ExerciseForm()
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        print(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            form.save()
            return redirect('exercise')
    context = {'form': form}
    return render(request, 'create_exercise.html', context)

# update the exercise
@login_required(login_url='login/')
def update_exercise(request, pk):
    exercise = Exercise.objects.get(id=pk)
    form = ExerciseForm(instance=exercise)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('exercise')

    context = {'form': form}
    return render(request, 'create_exercise.html', context)

# delete the exercise
@login_required(login_url='login/')
def delete_exercise(request, pk):
    exercise = Exercise.objects.get(id=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise')
    return render(request, 'delete.html', {'obj': exercise})

# edit user profile
@login_required(login_url='login/')
def edit_profile(request):
    user = request.user
    form = UserUpdateForm(instance=user)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, 'edit_profile.html', {'form': form })

# render the profile
@login_required(login_url='login/')
def profile(request):
    return render(request, 'profile.html')

# render past logged workouts
@login_required(login_url='login/')
def sessions(request):
    workouts = Workout.objects.filter(user=request.user)
    context = {
        'workouts': workouts,
    }
    return render(request, 'sessions.html', context)

# view logged workout details
@login_required(login_url='login/')
def workout_details(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    workout_exercises_details = WorkoutExerciseDetail.objects.filter(workout_exercise__in=workout_exercises)
    context = {
        'workout': workout,
        'workout_exercises': workout_exercises,
        'workout_exercises_details': workout_exercises_details
    }
    return render(request, 'workout_details.html', context)

# add exercise to your workout 
@login_required(login_url='login/')
def add_exercise(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    exercises = Exercise.objects.all()
    workout_exercises = WorkoutExercise.objects.filter(workout=workout)
    workout_exercises_details = WorkoutExerciseDetail.objects.filter(workout_exercise__in=workout_exercises)

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise')
        exercise = Exercise.objects.get(id=exercise_id)

        workout_exercise = WorkoutExercise.objects.create(workout=workout, exercise=exercise)

        sets = request.POST.get('sets')
        reps = request.POST.get('reps')
        weight = request.POST.get('weight')

        workout_exercise_detail = WorkoutExerciseDetail.objects.create(
            workout_exercise=workout_exercise,
            sets=sets,
            reps=reps,
            weight=weight
        )

        return redirect('add_workout', workout_id=workout_id)

    context = {
        'workout': workout,
        'exercises': exercises,
        'workout_exercises': workout_exercises,
        'workout_exercises_details': workout_exercises_details,
    }
    return render(request, 'add_workout_exercise.html', context)

# render the logger 
@login_required(login_url='login/')
def log(request):
    return render(request,'log.html')

# log my workouts
@login_required(login_url='login/')
def log_start(request):
    workout = Workout.objects.create(user=request.user)
    return redirect('add_workout', workout_id=workout.id)

# finish the workout and redirect to the sessions page
@login_required(login_url='login/')
def log_end(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if request.method == 'POST':
        workout.status = 'finished' 
        workout.date_completed = timezone.now()
        workout.save() 
        return redirect('sessions')
    context = {
        'workout': workout,
    }
    return render(request, 'log_end.html', context)

@login_required(login_url='login/')
def delete_workout(request, pk):
    workout = Workout.objects.get(id=pk)
    if request.method == "POST":
        workout.delete()
        return redirect('sessions')

