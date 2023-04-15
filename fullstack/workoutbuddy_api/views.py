from django.shortcuts import render, redirect
from .models import Exercise, Workout, WorkoutExercise, WorkoutExerciseDetail, Weight
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from .forms import ExerciseForm, UserUpdateForm, CurrentWeightForm
from django.utils import timezone
from django.http import JsonResponse

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

    # get q if found move on if not return ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    body_part = request.GET.get('body_part') if request.GET.get('body_part') != None else ''
    equipment = request.GET.get('equipment') if request.GET.get('equipment') != None else ''

    exercises = Exercise.objects.all()

    # if q is found filter exercises by name using icontains
    if q:
        exercises = exercises.filter(name__icontains=q)

    if body_part:
        exercises = exercises.filter(body_part=body_part)
    
    if equipment:
        exercises = exercises.filter(equipment=equipment)

    context = { 'exercises': exercises }
    return render(request, 'exercise.html', context)

# render the exercise details page
@login_required(login_url='login/')
def exercise_details(request, pk):
    exercise = Exercise.objects.get(id=pk)
    context = {'exercise': exercise}
    return render(request, 'exercise_details.html', context)

# render the workout exercises
@login_required(login_url='login/')
def workout_exercise_details(request, pk):
    workout_exercise = WorkoutExercise.objects.get(id=pk)
    exercise = workout_exercise.exercise
    context = {'exercise': exercise}
    return render(request, 'exercise_details.html', context)

# create exercise if form is valid
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

# update the exercise takes in exercise pk
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
    weight = Weight.objects.filter(user=request.user).last()

    if weight:
        start_weight = weight.start_weight
        current_weight = weight.current_weight
        goal_weight = weight.goal_weight
        progress = int(((current_weight - start_weight) / (goal_weight - start_weight)) * 100)

    else:
        start_weight = None
        current_weight = None
        goal_weight = None
        progress = None

    context = {
        'current_weight': current_weight,
        'goal_weight': goal_weight,
        'start_weight': start_weight,
        'progress': progress,
    }
    return render(request, 'profile.html', context)

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

# delete the exercise from the workout
@login_required(login_url='login/')
def remove_exercise(request, workout_id, exercise_id):
    workout_exercise = WorkoutExercise.objects.get(id=exercise_id)
    workout_exercise.delete()

    return redirect('add_workout', workout_id=workout_id)
    
# add exercise to your workout
# creates new workoutexercise and details objects with the exercise id
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
    if request.method == 'POST':
        workout_name = request.POST.get('workout_name')
        if workout_name:
            workout = Workout.objects.create(user=request.user, name=workout_name)
            return redirect('add_workout', workout_id=workout.id)
    return render(request, 'log_start.html')

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

# remove a workout from a session
@login_required(login_url='login/')
def delete_workout(request, pk):
    workout = Workout.objects.get(id=pk)
    if request.method == "POST":
        workout.delete()
        return redirect('sessions')

# retreive the sessions to populate the calendar
@login_required(login_url='login/')
def get_sessions(request):
    workouts = Workout.objects.filter(user=request.user)
    events = []
    for workout in workouts:
        events.append({
            'title': workout.name,
            'start': workout.date_completed.isoformat(),
            'url': f'/workout_details/{workout.id}'
        })
    print(events)
    return JsonResponse(events, safe=False)

# weight model request
# checks if it is post or get req
# if post it processes form data and updates weight object
# if get it renders the form with prepopulated data
@login_required(login_url='login/')
def add_update_current_weight(request):
    try:
        weight = Weight.objects.get(user=request.user)
    except Weight.DoesNotExist:
        weight = Weight(user=request.user, current_weight=0, goal_weight=0)

    if request.method == 'POST':
        form = CurrentWeightForm(request.POST, instance=weight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your weight has been updated.')
            return redirect('/profile/')
    else:
        form = CurrentWeightForm(instance=weight)
    
    context = {
        'form': form,
        'title': 'Add/Update Current Weight',
    }

    return render(request, 'add_update_current_weight.html', context)