# Generated by Django 5.1.3 on 2024-11-24 09:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gyms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password_hash', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('preference_id', models.AutoField(primary_key=True, serialize=False)),
                ('max_crowd_level', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_preferences', to='gyms.gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferences', to='users.user')),
            ],
        ),
    ]