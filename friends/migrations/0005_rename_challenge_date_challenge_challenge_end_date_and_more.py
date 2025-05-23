# Generated by Django 5.1.7 on 2025-04-29 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0004_challenge_challangeparticipation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='challenge_date',
            new_name='challenge_end_date',
        ),
        migrations.AlterField(
            model_name='challenge',
            name='workout_type',
            field=models.CharField(choices=[('Strength', 'Strength'), ('Cardio', 'Cardio'), ('Yoga', 'Yoga')], max_length=20),
        ),
    ]
