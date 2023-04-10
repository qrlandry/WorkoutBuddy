from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    username = None
    weight = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='workoutbuddy_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='workoutbuddy_user_permissions'
    )

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
    
