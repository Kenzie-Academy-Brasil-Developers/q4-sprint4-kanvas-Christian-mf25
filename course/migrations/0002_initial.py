# Generated by Django 4.0.4 on 2022-05-12 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
