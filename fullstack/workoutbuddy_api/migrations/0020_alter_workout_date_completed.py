# Generated by Django 4.2 on 2023-04-14 15:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workoutbuddy_api', '0019_alter_workout_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date_completed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]