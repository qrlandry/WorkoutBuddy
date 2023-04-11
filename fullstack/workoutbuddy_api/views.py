from django.shortcuts import render, redirect
from .serializers import UserSerializer, ExerciseSerializer, WorkoutSerializer, WorkoutExerciseSerializer, WorkoutExerciseDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Exercise, Workout, WorkoutExercise, WorkoutExerciseDetail
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .forms import ExerciseForm

class RegisterView(APIView):
    permission_classes=[AllowAny]
    queryset = User.objects.all()
    def post(self, req):
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        # Create JWT with user ID as the payload
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return Response({'jwt': token}, status=200)

# Checks if the session is valid and will throw an exception if the token is expired or invalid

class UserView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
            
    def get(self, request): 
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authentication header missing')
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except IndexError:
            raise AuthenticationFailed('Token prefix missing')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({'message': 'success'}, status=200)
    
class ExerciseListView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class WorkoutListCreateView(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutExerciseListCreateView(generics.ListCreateAPIView):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer

class WorkoutExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkoutExercise.objects.all()
    serializer_class = WorkoutExerciseSerializer

class WorkoutExerciseDetailListCreateView(generics.ListCreateAPIView):
    queryset = WorkoutExerciseDetail.objects.all()
    serializer_class = WorkoutExerciseDetailSerializer

class WorkoutExerciseDetailDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkoutExerciseDetail.objects.all()
    serializer_class = WorkoutExerciseDetailSerializer

def home(request):
    return render(request, 'home.html')

def exercise(request):
    exercises = Exercise.objects.all()
    context = { 'exercises': exercises }
    return render(request, 'exercise.html', context)

def exercise_details(request, pk):
    exercise = Exercise.objects.get(id=pk)
    context = {'exercise': exercise}
    return render(request, 'exercise_details.html', context)

def create_exercise(request):
    form = ExerciseForm()
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            print(form.save())
            return redirect('exercise')
    context = {'form': form}
    return render(request, 'create_exercise.html', context)

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

def delete_exercise(request, pk):
    exercise = Exercise.objects.get(id=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise')
    return render(request, 'delete.html', {'obj': exercise})

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def sessions(request):
    return render(request, 'sessions.html')

def log(request):
    return render(request, 'log.html')