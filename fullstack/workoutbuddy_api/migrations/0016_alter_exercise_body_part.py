# Generated by Django 4.2 on 2023-04-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutbuddy_api', '0015_alter_exercise_equipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='body_part',
            field=models.CharField(choices=[('Arms', 'Arms'), ('Shoulders', 'Shoulders'), ('Chest', 'Chest'), ('Core', 'Core'), ('Legs', 'Legs'), ('Back', 'Back'), ('Full body', 'Full Body')], max_length=150),
        ),
    ]
