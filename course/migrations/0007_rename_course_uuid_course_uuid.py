# Generated by Django 4.0.4 on 2022-05-18 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_rename_uuid_course_course_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_uuid',
            new_name='uuid',
        ),
    ]
