# Generated by Django 4.2 on 2023-04-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutbuddy_api', '0009_alter_user_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.IntegerField(null=True),
        ),
    ]
